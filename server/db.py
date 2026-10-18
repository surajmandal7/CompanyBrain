from __future__ import annotations

import json
import logging
from contextlib import contextmanager
from typing import Any, Iterable

import redis

from .config import Settings, get_settings

logger = logging.getLogger(__name__)


class GraphDatabaseError(RuntimeError):
    """Safe application-level database error with no credential details."""


class FalkorDB:
    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()
        self._client: redis.Redis | None = None

    def client(self) -> redis.Redis:
        if self._client is None:
            if not self.settings.db_configured:
                raise GraphDatabaseError("FalkorDB configuration is incomplete")
            connection_options = {
                "host": self.settings.falkordb_host,
                "port": self.settings.falkordb_port,
                "username": self.settings.falkordb_user,
                "password": self.settings.falkordb_password,
                "socket_timeout": self.settings.db_timeout_seconds,
                "socket_connect_timeout": self.settings.db_timeout_seconds,
                "health_check_interval": 30,
                "decode_responses": False,
            }
            if self.settings.falkordb_tls:
                connection_options.update({"ssl": True, "ssl_cert_reqs": None})
            self._client = redis.Redis(**connection_options)
        return self._client

    def query(self, cypher: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Run GRAPH.QUERY and normalize FalkorDB's RESP response into dictionaries."""
        try:
            command: list[Any] = ["GRAPH.QUERY", self.settings.graph_name, cypher]
            if params:
                command.extend(["--compact"])
            raw = self.client().execute_command(*command)
            return self._normalize(raw)
        except (redis.RedisError, TimeoutError, OSError) as exc:
            logger.warning("FalkorDB query failed: %s", type(exc).__name__)
            raise GraphDatabaseError("FalkorDB query failed") from exc

    def ping(self) -> bool:
        try:
            self.client().ping()
            self.query("RETURN 1 AS ok")
            return True
        except (GraphDatabaseError, redis.RedisError, TimeoutError, OSError):
            return False

    def _normalize(self, raw: Any) -> list[dict[str, Any]]:
        if not isinstance(raw, (list, tuple)) or len(raw) < 2:
            return []
        header = raw[0]
        rows = raw[1]
        if not isinstance(header, (list, tuple)) or not isinstance(rows, (list, tuple)):
            return []
        names = [self._decode(x) for x in header]
        output: list[dict[str, Any]] = []
        for row in rows:
            if not isinstance(row, (list, tuple)):
                continue
            output.append({names[i]: self._decode(row[i]) if i < len(row) else None for i in range(len(names))})
        return output

    @staticmethod
    def _decode(value: Any) -> Any:
        if isinstance(value, bytes):
            value = value.decode("utf-8", errors="replace")
        if isinstance(value, (list, tuple)):
            return [FalkorDB._decode(v) for v in value]
        if isinstance(value, dict):
            return {str(k): FalkorDB._decode(v) for k, v in value.items()}
        try:
            return json.loads(value) if isinstance(value, str) and value[:1] in "[{" else value
        except json.JSONDecodeError:
            return value


@contextmanager
def graph_db(settings: Settings | None = None):
    yield FalkorDB(settings)
