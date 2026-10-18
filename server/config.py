from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Iterable


@dataclass(frozen=True)
class Settings:
    graph_name: str
    falkordb_host: str
    falkordb_port: int
    falkordb_user: str
    falkordb_password: str
    gemini_api_key: str
    admin_api_key: str
    cors_origins: tuple[str, ...]
    falkordb_tls: bool = False
    db_timeout_seconds: float = 8.0

    @property
    def db_configured(self) -> bool:
        return bool(self.falkordb_host and self.falkordb_password and self.falkordb_port)

    @property
    def gemini_configured(self) -> bool:
        return bool(self.gemini_api_key)

    def public_status(self) -> dict[str, object]:
        return {
            "graph": self.graph_name,
            "databaseConfigured": self.db_configured,
            "aiConfigured": self.gemini_configured,
            "tls": self.falkordb_tls,
        }


def _required(name: str) -> str:
    return os.getenv(name, "").strip()


def _normalize_host(value: str) -> str:
    # FalkorDB Cloud commonly documents host:port together; redis-py receives the
    # port separately, so remove only a final numeric :port suffix.
    if value.count(":") == 1:
        host, maybe_port = value.rsplit(":", 1)
        if maybe_port.isdigit():
            return host
    return value


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    raw_port = _required("FALKORDB_PORT") or "50420"
    try:
        port = int(raw_port)
    except ValueError as exc:
        raise RuntimeError("FALKORDB_PORT must be a number") from exc
    origins = tuple(x.strip() for x in _required("CORS_ORIGINS").split(",") if x.strip())
    return Settings(
        graph_name=_required("FALKORDB_GRAPH_NAME") or "companyos",
        falkordb_host=_normalize_host(_required("FALKORDB_HOST")),
        falkordb_port=port,
        falkordb_user=_required("FALKORDB_USER") or "falkordb",
        falkordb_password=_required("FALKORDB_PASSWORD"),
        gemini_api_key=_required("GEMINI_API_KEY"),
        admin_api_key=_required("ADMIN_API_KEY"),
        cors_origins=origins or ("http://localhost:3000",),
        falkordb_tls=_required("FALKORDB_TLS").lower() in {"1", "true", "yes", "on"},
    )


def validate_runtime_settings(settings: Settings | None = None) -> list[str]:
    current = settings or get_settings()
    missing: list[str] = []
    for key, value in (
        ("FALKORDB_HOST", current.falkordb_host),
        ("FALKORDB_PASSWORD", current.falkordb_password),
        ("GEMINI_API_KEY", current.gemini_api_key),
        ("ADMIN_API_KEY", current.admin_api_key),
    ):
        if not value:
            missing.append(key)
    return missing
