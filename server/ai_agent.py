from __future__ import annotations

import json
import logging
from typing import Any

import httpx

from .config import get_settings
from .db import FalkorDB
from .graph_queries import context_for_operation
from .prompts import SYSTEM_ANSWER_PROMPT, SYSTEM_INTENT_PROMPT

logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
ALLOWED_OPERATIONS = {"dashboard", "projects", "employees", "tasks", "blocked_tasks", "decisions", "meetings", "policies", "documents", "knowledge_graph", "unknown"}


def _fallback_intent(question: str) -> tuple[str, str]:
    q = question.lower()
    project_names = ("phoenix", "atlas", "orion", "nova", "helix", "cedar", "polaris", "meridian", "ember", "quill", "solstice", "vela", "lighthouse", "horizon", "sentinel", "mosaic")
    project_entity = next((name for name in project_names if name in q), "")
    if "project" in q or project_entity:
        return "projects", project_entity
    if "leave" in q or "policy" in q:
        return "policies", ""
    if any(token in q for token in ("document", "file", "uploaded", "handbook", "brief", "notes")):
        return "documents", ""
    if "blocked" in q:
        return "blocked_tasks", ""
    if "project" in q or "owner" in q or "delayed" in q:
        return "projects", ""
    if "decision" in q or "why" in q:
        return "decisions", ""
    if "meeting" in q or "latest" in q:
        return "meetings", ""
    if "task" in q or "responsible" in q:
        return "tasks", ""
    if "who" in q or "employee" in q:
        return "employees", ""
    return "unknown", ""


async def _gemini(prompt: str) -> str:
    settings = get_settings()
    if not settings.gemini_configured:
        raise RuntimeError("Gemini is not configured")
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent"
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.1, "responseMimeType": "application/json"}}
    async with httpx.AsyncClient(timeout=18.0) as client:
        response = await client.post(url, headers={"x-goog-api-key": settings.gemini_api_key}, json=payload)
        response.raise_for_status()
        data = response.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]


async def classify(question: str) -> tuple[str, str]:
    fallback = _fallback_intent(question)
    if fallback[0] != "unknown":
        return fallback
    try:
        raw = await _gemini(SYSTEM_INTENT_PROMPT.format(question=question[:1200]))
        parsed = json.loads(raw)
        operation = parsed.get("operation", "unknown")
        entity = str(parsed.get("entity", ""))[:80]
        return (operation if operation in ALLOWED_OPERATIONS else fallback[0], entity)
    except Exception as exc:
        logger.info("Gemini intent fallback: %s", type(exc).__name__)
        return fallback


async def answer_question(db: FalkorDB, question: str) -> dict[str, Any]:
    operation, entity = await classify(question)
    if operation == "unknown":
        return {"answer": "I can answer questions about Nexora people, projects, tasks, meetings, decisions, uploaded documents, policies, and the knowledge graph. Try asking about Project Phoenix, blocked tasks, or a document you uploaded.", "citations": [], "operation": operation}
    context = context_for_operation(db, operation, entity)
    if not context:
        return {"answer": "I couldn’t find enough verified company data to answer that question.", "citations": [], "operation": operation}
    serial = json.dumps(context[:40], ensure_ascii=False, default=str)
    try:
        raw = await _gemini(SYSTEM_ANSWER_PROMPT.format(context=serial, question=question[:1200]))
        parsed = json.loads(raw)
        answer = str(parsed.get("answer", "")).strip()
        requested_ids = {str(item) for item in parsed.get("citationIds", [])}
    except Exception as exc:
        logger.info("Gemini answer fallback: %s", type(exc).__name__)
        answer = _deterministic_answer(question, context)
        requested_ids = set()
    # High-confidence operational questions are answered from the returned rows
    # directly so a provider response cannot contradict a verified relationship.
    if any(marker in question.lower() for marker in ("who owns", "owner of", "responsible for", "blocked", "leave policy")):
        answer = _deterministic_answer(question, context)
        if "who owns" in question.lower() or "owner of" in question.lower():
            requested_ids = {str(_focused_row(question, context).get("id"))}
    flattened = _flatten_records(context)
    valid = {str(row.get("id")): row for row in flattened if row.get("id")}
    citation_ids = requested_ids & valid.keys()
    if not citation_ids:
        citation_ids = set(list(valid.keys())[:4])
    focused_records = _flatten_records([_focused_row(question, context)]) if context else flattened
    document_ids = [str(row["id"]) for row in focused_records if row.get("sourceRef") and row.get("id")]
    for document_id in document_ids[:4]:
        citation_ids.add(document_id)
    citations = [_citation(valid[ident], operation) for ident in citation_ids if ident in valid]
    return {"answer": answer or _deterministic_answer(question, context), "citations": citations, "operation": operation, "contextRecordCount": len(flattened)}


def _citation_label(row: dict[str, Any]) -> str:
    return str(row.get("name") or row.get("title") or row.get("id"))


def _citation(row: dict[str, Any], operation: str) -> dict[str, Any]:
    documents: list[Any] = list(row.get("documents") or []) if isinstance(row.get("documents"), list) else []
    source_documents = [document for document in documents if isinstance(document, dict) and document.get("sourceRef")]
    is_project = bool(row.get("owner") and row.get("name"))
    return {
        "id": str(row.get("id")),
        "label": _citation_label(row),
        "type": str(row.get("sourceType") or row.get("type") or operation),
        "kind": "Project" if is_project else ("Document" if row.get("sourceRef") else str(row.get("type") or operation)),
        "sourceRef": row.get("sourceRef"),
        "sourceType": row.get("sourceType"),
        "sourceRefs": [str(document.get("sourceRef")) for document in source_documents],
        "sourceLabels": [str(document.get("title")) for document in source_documents if document.get("title")],
    }


def _flatten_records(context: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Flatten composite graph context for safe citation validation."""
    result: list[dict[str, Any]] = []
    seen: set[str] = set()

    def visit(value: Any) -> None:
        if isinstance(value, dict):
            ident = str(value.get("id")) if value.get("id") else ""
            if ident and ident not in seen:
                seen.add(ident)
                result.append(value)
            for nested in value.values():
                if isinstance(nested, (dict, list)):
                    visit(nested)
        elif isinstance(value, list):
            for item in value:
                visit(item)

    visit(context)
    return result


def _deterministic_answer(question: str, context: list[dict[str, Any]]) -> str:
    q = question.lower()
    first = _focused_row(question, context)
    if first.get("owner") and ("project" in q or "owner" in q or first.get("tasks")):
        owner_value = first.get("owner")
        owner_name = str(owner_value.get("name") if isinstance(owner_value, dict) else owner_value or "an assigned owner")
        team_names = [str(team) for team in first.get("teams", []) if team]
        task_rows = [task for task in first.get("tasks", []) if isinstance(task, dict)]
        blocked = [task for task in task_rows if str(task.get("status")) == "Blocked"]
        decisions = [decision for decision in first.get("decisions", []) if isinstance(decision, dict)]
        documents = [document for document in first.get("documents", []) if isinstance(document, dict) and document.get("title")]
        task_summary = "; ".join(f"{task.get('title')} ({task.get('status')}, due {task.get('dueDate')})" for task in task_rows[:5]) or "No linked tasks were returned."
        decision_summary = "; ".join(f"{decision.get('title')} ({decision.get('date')})" for decision in decisions[:3]) or "No linked decision was returned."
        source_summary = ", ".join(str(document.get("title")) for document in documents[:4]) or "No linked source document was returned."
        team_summary = ", ".join(team_names) or "No supporting team was returned."
        risk_note = f" There are {len(blocked)} blocked task(s) in this project." if blocked else ""
        return f"{first.get('name', 'The project')} is {first.get('status', 'in the graph')} with priority {first.get('priority', 'unspecified')} and a due date of {first.get('dueDate', 'unspecified')}. It is owned by {owner_name} and supported by {team_summary}.{risk_note}\n\nLinked work: {task_summary}\n\nDecision trail: {decision_summary}\n\nSource document(s) used: {source_summary}."
    if ("owner" in q or "owns" in q) and first.get("owner"):
        return f"{first.get('name', 'That project')} is owned by {first['owner']}."
    if "leave policy" in q and first.get("summary"):
        return f"{first.get('name', 'The leave policy')}: {first['summary']}"
    if "blocked" in q:
        blocked = [task for row in context for task in row.get("tasks", []) if isinstance(task, dict) and str(task.get("status")) == "Blocked"]
        if blocked:
            details = "; ".join(f"{task.get('title')} ({task.get('priority')}, due {task.get('dueDate')})" for task in blocked[:6])
            return f"I found {len(blocked)} blocked task(s) across the connected project context: {details}."
        return "I did not find a blocked task in the connected graph context."
    label = first.get("name") or first.get("title") or "the matching record"
    return f"The graph contains verified information about {label}. See the cited records for the supporting details."


def _focused_row(question: str, context: list[dict[str, Any]]) -> dict[str, Any]:
    q = question.lower()
    for row in context:
        label = str(row.get("name") or row.get("title") or "").lower()
        if label and any(token in label and token in q for token in ("phoenix", "leave", "atlas", "orion", "nova", "helix", "cedar", "polaris", "meridian", "ember", "quill", "solstice", "vela", "lighthouse", "horizon", "sentinel", "mosaic")):
            return row
    for row in context:
        if "at risk" in q and str(row.get("status", "")).lower() == "at risk":
            return row
    return context[0]
