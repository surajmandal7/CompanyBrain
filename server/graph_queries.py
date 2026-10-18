from __future__ import annotations

from typing import Any

from .db import FalkorDB


def _safe_term(term: str | None) -> str:
    value = (term or "").strip()[:80]
    return value.replace("\\", "\\\\").replace("'", "\\'")


def dashboard(db: FalkorDB) -> dict[str, Any]:
    counts = db.query("""
        MATCH (n)
        RETURN labels(n)[0] AS label, count(n) AS total
    """)
    count_map = {str(row.get("label")): int(row.get("total") or 0) for row in counts}
    task_status = db.query("""
        MATCH (t:Task)
        RETURN t.status AS status, count(t) AS total
    """)
    status_map = {str(row.get("status")): int(row.get("total") or 0) for row in task_status}
    decisions = db.query("""
        MATCH (d:Decision)
        RETURN d.id AS id, d.title AS title, d.date AS date, d.status AS status, d.reason AS reason
        ORDER BY d.date DESC LIMIT 4
    """)
    meetings = db.query("""
        MATCH (m:Meeting)
        RETURN m.id AS id, m.title AS title, m.date AS date, m.summary AS summary
        ORDER BY m.date DESC LIMIT 4
    """)
    return {
        "counts": {
            "employees": count_map.get("Employee", 0),
            "teams": count_map.get("Team", 0),
            "projects": count_map.get("Project", 0),
            "tasks": count_map.get("Task", 0),
            "meetings": count_map.get("Meeting", 0),
            "decisions": count_map.get("Decision", 0),
            "documents": count_map.get("Document", 0),
            "policies": count_map.get("Policy", 0),
            "nodes": sum(count_map.values()),
        },
        "tasks": {
            "open": status_map.get("Open", 0) + status_map.get("In Progress", 0),
            "blocked": status_map.get("Blocked", 0),
            "done": status_map.get("Done", 0),
            "byStatus": status_map,
        },
        "decisions": decisions,
        "meetings": meetings,
    }


def projects(db: FalkorDB, search: str | None = None) -> list[dict[str, Any]]:
    term = _safe_term(search)
    where = f"WHERE toLower(p.name) CONTAINS toLower('{term}')" if term else ""
    return db.query(f"""
        MATCH (p:Project)
        {where}
        OPTIONAL MATCH (owner:Employee)-[:OWNS]->(p)
        OPTIONAL MATCH (p)-[:HAS_TASK]->(t:Task)
        RETURN p.id AS id, p.name AS name, p.status AS status, p.priority AS priority,
               p.description AS description, p.dueDate AS dueDate, owner.name AS owner,
               count(t) AS taskCount
        ORDER BY p.name
    """)


def project_context(db: FalkorDB, search: str | None = None) -> list[dict[str, Any]]:
    term = _safe_term(search)
    where = f"WHERE toLower(p.name) CONTAINS toLower('{term}') OR toLower(p.description) CONTAINS toLower('{term}')" if term else ""
    rows = db.query(f"""
        MATCH (p:Project)
        {where}
        OPTIONAL MATCH (owner:Employee)-[:OWNS]->(p)
        OPTIONAL MATCH (owner)-[:MEMBER_OF]->(team:Team)
        WITH p, owner, collect(DISTINCT team.name) AS teams
        OPTIONAL MATCH (p)-[:HAS_TASK]->(t:Task)
        WITH p, owner, teams, collect(DISTINCT CASE WHEN t.id IS NOT NULL THEN t.id + '|' + t.title + '|' + t.status + '|' + t.priority + '|' + t.dueDate ELSE '' END) AS taskRows
        OPTIONAL MATCH (p)-[:HAS_DECISION]->(d:Decision)
        WITH p, owner, teams, taskRows, collect(DISTINCT CASE WHEN d.id IS NOT NULL THEN d.id + '|' + d.title + '|' + d.date + '|' + d.status + '|' + d.reason ELSE '' END) AS decisionRows
        OPTIONAL MATCH (p)-[:DOCUMENTED_IN]->(doc:Document)
        RETURN p.id AS id, p.name AS name, p.status AS status, p.priority AS priority,
               p.description AS description, p.dueDate AS dueDate,
               owner.id AS ownerId, owner.name AS ownerName, owner.role AS ownerRole,
               teams, taskRows, decisionRows,
               collect(DISTINCT CASE WHEN doc.id IS NOT NULL THEN doc.id + '|' + doc.title + '|' + doc.sourceType + '|' + doc.sourceRef + '|' + coalesce(doc.summary, '') ELSE '' END) AS documentRows
        ORDER BY p.name
    """)
    output: list[dict[str, Any]] = []
    for row in rows:
        def as_list(value: Any) -> list[Any]:
            if isinstance(value, (list, tuple)):
                return list(value)
            text = str(value or "").strip()
            if text.startswith("[") and text.endswith("]"):
                inner = text[1:-1].strip()
                return [] if not inner else [part.strip() for part in inner.split(", ")]
            return [value] if value else []

        def split_rows(key: str, fields: int) -> list[list[str]]:
            values = as_list(row.get(key))
            parsed: list[list[str]] = []
            for value in values:
                if not value:
                    continue
                parts = str(value).split("|", fields - 1)
                if len(parts) == fields:
                    parsed.append(parts)
            return parsed

        output.append({
            "id": row.get("id"), "name": row.get("name"), "status": row.get("status"),
            "priority": row.get("priority"), "description": row.get("description"), "dueDate": row.get("dueDate"),
            "owner": {"id": row.get("ownerId"), "name": row.get("ownerName"), "role": row.get("ownerRole")},
            "teams": [str(team) for team in as_list(row.get("teams")) if team],
            "tasks": [{"id": parts[0], "title": parts[1], "status": parts[2], "priority": parts[3], "dueDate": parts[4]} for parts in split_rows("taskRows", 5)],
            "decisions": [{"id": parts[0], "title": parts[1], "date": parts[2], "status": parts[3], "reason": parts[4]} for parts in split_rows("decisionRows", 5)],
            "documents": [{"id": parts[0], "title": parts[1], "sourceType": parts[2], "sourceRef": parts[3], "summary": parts[4]} for parts in split_rows("documentRows", 5)],
        })
    return output


def employees(db: FalkorDB, search: str | None = None) -> list[dict[str, Any]]:
    term = _safe_term(search)
    where = f"WHERE toLower(e.name) CONTAINS toLower('{term}') OR toLower(e.role) CONTAINS toLower('{term}')" if term else ""
    return db.query(f"""
        MATCH (e:Employee)
        {where}
        OPTIONAL MATCH (e)-[:MEMBER_OF]->(team:Team)
        RETURN e.id AS id, e.name AS name, e.role AS role, e.email AS email,
               e.location AS location, team.name AS team
        ORDER BY e.name
    """)


def tasks(db: FalkorDB, search: str | None = None, blocked_only: bool = False) -> list[dict[str, Any]]:
    term = _safe_term(search)
    clauses = []
    if term:
        clauses.append("(toLower(t.title) CONTAINS toLower('{0}') OR toLower(t.status) CONTAINS toLower('{0}'))".format(term))
    if blocked_only:
        clauses.append("t.status = 'Blocked'")
    where = "WHERE " + " AND ".join(clauses) if clauses else ""
    return db.query(f"""
        MATCH (t:Task)
        {where}
        OPTIONAL MATCH (owner:Employee)-[:ASSIGNED_TO]->(t)
        OPTIONAL MATCH (p:Project)-[:HAS_TASK]->(t)
        RETURN t.id AS id, t.title AS title, t.status AS status, t.priority AS priority,
               t.dueDate AS dueDate, t.description AS description, owner.name AS owner,
               p.name AS project
        ORDER BY CASE t.status WHEN 'Blocked' THEN 0 WHEN 'In Progress' THEN 1 ELSE 2 END, t.dueDate
    """)


def decisions(db: FalkorDB, search: str | None = None) -> list[dict[str, Any]]:
    term = _safe_term(search)
    where = f"WHERE toLower(d.title) CONTAINS toLower('{term}') OR toLower(d.reason) CONTAINS toLower('{term}')" if term else ""
    return db.query(f"""
        MATCH (d:Decision)
        {where}
        OPTIONAL MATCH (m:Meeting)-[:RECORDED_DECISION]->(d)
        RETURN d.id AS id, d.title AS title, d.date AS date, d.status AS status, d.reason AS reason,
               m.title AS meeting
        ORDER BY d.date DESC
    """)


def meetings(db: FalkorDB) -> list[dict[str, Any]]:
    return db.query("""
        MATCH (m:Meeting)
        OPTIONAL MATCH (m)-[:RECORDED_DECISION]->(d:Decision)
        RETURN m.id AS id, m.title AS title, m.date AS date, m.summary AS summary,
               collect(d.title) AS decisions
        ORDER BY m.date DESC
    """)


def policies(db: FalkorDB) -> list[dict[str, Any]]:
    return db.query("""
        MATCH (p:Policy)
        OPTIONAL MATCH (p)-[:DOCUMENTED_IN]->(d:Document)
        RETURN p.id AS id, p.name AS name, p.summary AS summary, p.updatedAt AS updatedAt,
               d.title AS document
        ORDER BY p.name
    """)


def documents(db: FalkorDB, search: str | None = None) -> list[dict[str, Any]]:
    term = _safe_term(search)
    where = f"WHERE toLower(d.title) CONTAINS toLower('{term}') OR toLower(d.filename) CONTAINS toLower('{term}') OR toLower(d.extractedText) CONTAINS toLower('{term}')" if term else ""
    return db.query(f"""
        MATCH (d:Document)
        {where}
        RETURN d.id AS id, d.title AS title, d.filename AS filename, d.sourceType AS sourceType,
               d.sourceRef AS sourceRef, d.mimeType AS mimeType, d.sizeBytes AS sizeBytes,
               d.uploadedAt AS uploadedAt, d.textLength AS textLength, d.contentTruncated AS contentTruncated
        ORDER BY d.uploadedAt DESC, d.title
    """)


def document_context(db: FalkorDB, search: str | None = None) -> list[dict[str, Any]]:
    term = _safe_term(search)
    where = f"WHERE toLower(d.title) CONTAINS toLower('{term}') OR toLower(d.filename) CONTAINS toLower('{term}') OR toLower(d.extractedText) CONTAINS toLower('{term}')" if term else ""
    return db.query(f"""
        MATCH (d:Document)
        {where}
        RETURN d.id AS id, d.title AS title, d.filename AS filename, d.sourceRef AS sourceRef,
               substring(d.extractedText, 0, 4000) AS content, d.uploadedAt AS uploadedAt
        ORDER BY d.uploadedAt DESC LIMIT 8
    """)


def knowledge_graph(db: FalkorDB) -> dict[str, Any]:
    nodes = db.query("""
        MATCH (n)
        WHERE labels(n)[0] IN ['Employee','Team','Project','Task','Decision','Meeting','Document']
        RETURN n.id AS id, labels(n)[0] AS type, coalesce(n.name, n.title) AS label,
               coalesce(n.status, '') AS status
    """)
    links = db.query("""
        MATCH (a)-[r]->(b)
        WHERE labels(a)[0] IN ['Employee','Team','Project','Task','Decision','Meeting','Document']
          AND labels(b)[0] IN ['Employee','Team','Project','Task','Decision','Meeting','Document']
        RETURN a.id AS source, b.id AS target, type(r) AS relationship
    """)
    return {"nodes": nodes, "links": links}


def context_for_operation(db: FalkorDB, operation: str, entity: str = "") -> list[dict[str, Any]]:
    if operation == "projects":
        return project_context(db, entity)
    if operation == "employees":
        return employees(db, entity)
    if operation in {"tasks", "blocked_tasks"}:
        return tasks(db, entity, blocked_only=operation == "blocked_tasks")
    if operation == "decisions":
        return decisions(db, entity)
    if operation == "meetings":
        return meetings(db)
    if operation == "policies":
        return policies(db)
    if operation in {"documents", "document_context"}:
        return document_context(db, entity)
    if operation == "knowledge_graph":
        return knowledge_graph(db).get("nodes", [])
    if operation == "dashboard":
        return [dashboard(db)]
    return []
