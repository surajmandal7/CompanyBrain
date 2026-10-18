from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from fastapi import Depends, FastAPI, File, Header, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .ai_agent import answer_question
from .config import get_settings, validate_runtime_settings
from .db import FalkorDB, GraphDatabaseError
from .document_ingest import MAX_BATCH_BYTES, MAX_UPLOAD_BYTES, ingest_document
from .graph_queries import dashboard, decisions, documents, employees, knowledge_graph, meetings, projects, tasks
from .seed_data import seed_graph

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")
logger = logging.getLogger("companybrain")
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(title="Company Brain API", version="1.0.0", docs_url="/api/docs")
settings = get_settings()
app.add_middleware(CORSMiddleware, allow_origins=list(settings.cors_origins), allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["Content-Type", "X-Admin-Key"], max_age=600)


class ChatRequest(BaseModel):
    question: str = Field(min_length=2, max_length=1200)


class SeedRequest(BaseModel):
    confirm: bool = False


def get_db() -> FalkorDB:
    return FalkorDB()


def require_admin(x_admin_key: str | None = Header(default=None)) -> None:
    if not settings.admin_api_key or x_admin_key != settings.admin_api_key:
        raise HTTPException(status_code=401, detail="Valid admin access is required")


@app.middleware("http")
async def request_limits(request: Request, call_next):
    if request.method == "POST" and request.headers.get("content-length"):
        try:
            limit = MAX_BATCH_BYTES + 1_000 if request.url.path == "/api/documents/upload" else 64_000
            if int(request.headers["content-length"]) > limit:
                return JSONResponse(status_code=413, content={"detail": "Request body is too large"})
        except ValueError:
            return JSONResponse(status_code=400, content={"detail": "Invalid content length"})
    return await call_next(request)


@app.get("/api/health")
def health(db: FalkorDB = Depends(get_db)):
    missing = validate_runtime_settings(settings)
    connected = db.ping() if not missing else False
    return {"status": "ok" if connected else "degraded", "databaseConnected": connected, "missingConfiguration": missing, "configuration": settings.public_status()}


@app.get("/api/dashboard")
def get_dashboard(db: FalkorDB = Depends(get_db)):
    try:
        return dashboard(db)
    except GraphDatabaseError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.get("/api/projects")
def get_projects(search: str | None = None, db: FalkorDB = Depends(get_db)):
    try:
        return {"items": projects(db, search)}
    except GraphDatabaseError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.get("/api/employees")
def get_employees(search: str | None = None, db: FalkorDB = Depends(get_db)):
    try:
        return {"items": employees(db, search)}
    except GraphDatabaseError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.get("/api/tasks")
def get_tasks(search: str | None = None, blocked: bool = False, db: FalkorDB = Depends(get_db)):
    try:
        return {"items": tasks(db, search, blocked_only=blocked)}
    except GraphDatabaseError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.get("/api/decisions")
def get_decisions(search: str | None = None, db: FalkorDB = Depends(get_db)):
    try:
        return {"items": decisions(db, search)}
    except GraphDatabaseError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.get("/api/meetings")
def get_meetings(db: FalkorDB = Depends(get_db)):
    try:
        return {"items": meetings(db)}
    except GraphDatabaseError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.get("/api/documents")
def get_documents(search: str | None = None, db: FalkorDB = Depends(get_db)):
    try:
        return {"items": documents(db, search)}
    except GraphDatabaseError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.post("/api/documents/upload", dependencies=[Depends(require_admin)])
async def upload_document(
    files: list[UploadFile] | None = File(default=None),
    file: UploadFile | None = File(default=None),
    db: FalkorDB = Depends(get_db),
):
    selected = list(files or [])
    if file is not None:
        selected.append(file)
    if not selected:
        raise HTTPException(status_code=400, detail="Choose at least one file to upload")
    stored: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []
    total_bytes = 0
    for upload in selected:
        name = upload.filename or "unnamed file"
        content = await upload.read(MAX_UPLOAD_BYTES + 1)
        total_bytes += len(content)
        if total_bytes > MAX_BATCH_BYTES:
            errors.append({"filename": name, "error": "The batch exceeds the 50 MB total limit."})
            continue
        try:
            stored.append(ingest_document(db, name, content, upload.content_type))
        except ValueError as exc:
            errors.append({"filename": name, "error": str(exc)})
        except GraphDatabaseError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
    if not stored:
        detail = "; ".join(f"{item['filename']}: {item['error']}" for item in errors) or "No files were stored"
        raise HTTPException(status_code=400, detail=detail)
    return {"status": "stored" if not errors else "partial", "documents": stored, "errors": errors, "storedCount": len(stored), "errorCount": len(errors)}


@app.get("/api/knowledge-graph")
def get_knowledge_graph(db: FalkorDB = Depends(get_db)):
    try:
        return knowledge_graph(db)
    except GraphDatabaseError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.post("/api/chat")
async def chat(payload: ChatRequest, db: FalkorDB = Depends(get_db)):
    try:
        return await answer_question(db, payload.question)
    except GraphDatabaseError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        logger.warning("Chat request failed: %s", type(exc).__name__)
        raise HTTPException(status_code=502, detail="The assistant could not complete that request") from exc


@app.post("/api/admin/seed", dependencies=[Depends(require_admin)])
def seed(payload: SeedRequest, db: FalkorDB = Depends(get_db)):
    if not payload.confirm:
        raise HTTPException(status_code=400, detail="Set confirm=true to run the idempotent seed")
    try:
        return {"status": "completed", "graph": settings.graph_name, **seed_graph(db)}
    except GraphDatabaseError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.get("/api/settings")
def get_settings_status():
    return {"graph": settings.graph_name, "configuration": settings.public_status(), "seedEndpoint": "/api/admin/seed"}


@app.get("/manus-routes.json")
def route_manifest():
    manifest = BASE_DIR / "public" / "manus-routes.json"
    return JSONResponse(content=__import__("json").loads(manifest.read_text()))


DIST = BASE_DIR / "frontend" / "dist"
if DIST.exists():
    app.mount("/assets", StaticFiles(directory=DIST / "assets"), name="assets")


@app.get("/{path:path}")
def frontend(path: str):
    if path.startswith("api/"):
        raise HTTPException(status_code=404, detail="Not found")
    candidate = DIST / path
    if path and candidate.is_file():
        return FileResponse(candidate)
    index = DIST / "index.html"
    if index.exists():
        return FileResponse(index)
    return JSONResponse(status_code=503, content={"detail": "Frontend build is not ready"})
