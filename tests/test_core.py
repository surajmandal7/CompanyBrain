from server.ai_agent import _fallback_intent, _flatten_records
from server.config import Settings, _normalize_host, validate_runtime_settings


def test_host_normalization_removes_only_trailing_port():
    assert _normalize_host("graph.example:50420") == "graph.example"
    assert _normalize_host("graph.example") == "graph.example"


def test_settings_validation_does_not_expose_values():
    settings = Settings("companyos", "host", 50420, "falkordb", "secret", "gemini", "admin", ("http://localhost",))
    assert validate_runtime_settings(settings) == []
    assert "secret" not in str(settings.public_status())


def test_intent_fallback_is_allowlisted():
    assert _fallback_intent("Which tasks are currently blocked?")[0] == "blocked_tasks"
    assert _fallback_intent("What is our company leave policy?")[0] == "policies"
    assert _fallback_intent("make up an answer")[0] == "unknown"


def test_composite_context_flattens_nested_source_documents_once():
    context = [{
        "id": "proj-nova",
        "name": "Project Nova",
        "owner": {"id": "emp-victor", "name": "Victor Petrov"},
        "tasks": [{"id": "task-nova-pipeline", "title": "Consolidate telemetry"}],
        "documents": [{"id": "doc-nova-charter", "title": "Nova charter", "sourceRef": "nexora://projects/nova-charter"}],
    }]
    flattened = _flatten_records(context)
    assert [row["id"] for row in flattened] == ["proj-nova", "emp-victor", "task-nova-pipeline", "doc-nova-charter"]
