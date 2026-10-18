from __future__ import annotations

import hashlib
import io
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .db import FalkorDB

ALLOWED_EXTENSIONS = {".txt", ".md", ".markdown", ".json", ".pdf", ".docx"}
MAX_UPLOAD_BYTES = 10 * 1024 * 1024
MAX_BATCH_BYTES = 50 * 1024 * 1024
MAX_EXTRACTED_CHARS = 250_000
CHUNK_SIZE = 12_000


def _cypher_string(value: Any) -> str:
    return json.dumps(str(value), ensure_ascii=False)


def _clean_text(value: str) -> str:
    value = value.replace("\x00", " ")
    value = re.sub(r"\r\n?", "\n", value)
    value = re.sub(r"[ \t]+\n", "\n", value)
    return value.strip()


def extract_text(filename: str, content: bytes) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise ValueError("Unsupported file type. Use TXT, Markdown, JSON, PDF, or DOCX.")
    if suffix in {".txt", ".md", ".markdown"}:
        return _clean_text(content.decode("utf-8-sig", errors="replace"))
    if suffix == ".json":
        try:
            parsed = json.loads(content.decode("utf-8-sig"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("The JSON file is not valid UTF-8 JSON.") from exc
        return _clean_text(json.dumps(parsed, ensure_ascii=False, indent=2))
    if suffix == ".pdf":
        from pypdf import PdfReader

        reader = PdfReader(io.BytesIO(content))
        return _clean_text("\n\n".join(page.extract_text() or "" for page in reader.pages))
    from docx import Document

    document = Document(io.BytesIO(content))
    return _clean_text("\n\n".join(paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()))


def ingest_document(db: FalkorDB, filename: str, content: bytes, content_type: str | None = None) -> dict[str, Any]:
    if len(content) > MAX_UPLOAD_BYTES:
        raise ValueError("Files must be 10 MB or smaller.")
    extracted = extract_text(filename, content)
    if not extracted:
        raise ValueError("No readable text was found in that file.")
    digest = hashlib.sha256(content).hexdigest()
    document_id = f"doc-upload-{digest[:24]}"
    now = datetime.now(timezone.utc).isoformat()
    stored_text = extracted[:MAX_EXTRACTED_CHARS]
    truncated = len(extracted) > MAX_EXTRACTED_CHARS
    title = Path(filename).stem.replace("_", " ").replace("-", " ").strip() or filename
    props = {
        "id": document_id,
        "title": title[:180],
        "filename": filename[:255],
        "sourceType": "Uploaded JSON" if Path(filename).suffix.lower() == ".json" else "Uploaded document",
        "sourceRef": f"upload://{document_id}",
        "mimeType": content_type or "application/octet-stream",
        "sizeBytes": len(content),
        "checksum": digest,
        "uploadedAt": now,
        "extractedText": stored_text,
        "textLength": len(extracted),
        "contentTruncated": truncated,
    }
    assignments = ", ".join(f"{key}: {_cypher_string(value)}" for key, value in props.items())
    db.query(f"MERGE (d:Document {{id: {_cypher_string(document_id)}}}) SET d += {{{assignments}}} RETURN d.id AS id")
    for position, start in enumerate(range(0, len(extracted), CHUNK_SIZE)):
        chunk_id = f"{document_id}-chunk-{position + 1}"
        chunk = extracted[start : start + CHUNK_SIZE]
        db.query(
            f"MERGE (c:DocumentChunk {{id: {_cypher_string(chunk_id)}}}) "
            f"SET c += {{id: {_cypher_string(chunk_id)}, documentId: {_cypher_string(document_id)}, position: {position + 1}, content: {_cypher_string(chunk)}}} "
            f"WITH c MATCH (d:Document {{id: {_cypher_string(document_id)}}}) MERGE (d)-[:HAS_CHUNK]->(c) RETURN c.id AS id"
        )
    return {
        "id": document_id,
        "title": title[:180],
        "filename": filename,
        "checksum": digest,
        "sizeBytes": len(content),
        "textLength": len(extracted),
        "chunks": max(1, (len(extracted) + CHUNK_SIZE - 1) // CHUNK_SIZE),
        "contentTruncated": truncated,
        "sourceRef": f"upload://{document_id}",
    }
