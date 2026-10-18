from server.document_ingest import MAX_UPLOAD_BYTES, extract_text, ingest_document


def test_extract_text_supports_plain_text_and_rejects_unknown_types():
    assert "Rahul" in extract_text("brief.txt", b"Owner: Rahul")
    assert "Markdown" in extract_text("notes.md", b"# Markdown")
    assert '"owner": "Rahul"' in extract_text("record.json", b'{"owner":"Rahul"}')
    try:
        extract_text("image.png", b"x")
    except ValueError as exc:
        assert "Unsupported file type" in str(exc)
    else:
        raise AssertionError("unsupported file should be rejected")

    try:
        extract_text("broken.json", b"{not-json}")
    except ValueError as exc:
        assert "valid UTF-8 JSON" in str(exc)
    else:
        raise AssertionError("invalid JSON should be rejected")


def test_upload_limit_is_explicit():
    assert MAX_UPLOAD_BYTES == 10 * 1024 * 1024


def test_ingest_requires_readable_text():
    class UnusedDb:
        pass
    try:
        ingest_document(UnusedDb(), "empty.txt", b"   ")
    except ValueError as exc:
        assert "No readable text" in str(exc)
    else:
        raise AssertionError("empty document should be rejected")
