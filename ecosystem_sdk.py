"""Minimal integration SDK template for read-only ecosystem metrics."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class EcosystemClient:
    base_url: str
    api_key: str | None = None

    def build_metrics_request(self, project: str) -> dict[str, Any]:
        """Return a request description; this template does not send it."""
        if not project or any(char.isspace() for char in project):
            raise ValueError("project must be a non-empty identifier")
        return {"method": "GET", "url": f"{self.base_url.rstrip('/')}/v1/projects/{project}/metrics", "headers": {}, "secret_required": bool(self.api_key), "read_only": True}

    def build_events_request(self, project: str) -> dict[str, Any]:
        return {"method": "GET", "url": f"{self.base_url.rstrip('/')}/v1/projects/{project}/events", "read_only": True}
