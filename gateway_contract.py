"""Authenticated, rate-limited contract for the public FOX Studio gateway.

This module only validates and describes requests. It does not move funds,
invoke blockchain signers, or expose private repository data.
"""
from __future__ import annotations

import hashlib
import hmac
import time
from dataclasses import dataclass, field
from typing import Mapping

ALLOWED_ROUTES: dict[str, frozenset[str]] = {
    "/v1/studio/status": frozenset({"GET"}),
    "/v1/studio/capabilities": frozenset({"GET"}),
    "/v1/creators/submissions": frozenset({"POST"}),
}


def canonical_payload(method: str, path: str, timestamp: str, body: bytes = b"") -> bytes:
    body_digest = hashlib.sha256(body).hexdigest()
    return "\n".join((method.upper(), path, timestamp, body_digest)).encode("utf-8")


def sign_request(secret: str, method: str, path: str, timestamp: str, body: bytes = b"") -> str:
    if not secret:
        raise ValueError("gateway secret is required")
    return hmac.new(secret.encode("utf-8"), canonical_payload(method, path, timestamp, body), hashlib.sha256).hexdigest()


def verify_request(
    *,
    secret: str,
    method: str,
    path: str,
    timestamp: str,
    signature: str,
    body: bytes = b"",
    now: int | None = None,
    max_skew_seconds: int = 300,
) -> bool:
    """Verify an allow-listed request with a short-lived HMAC signature."""
    allowed_methods = ALLOWED_ROUTES.get(path)
    if not allowed_methods or method.upper() not in allowed_methods:
        return False
    try:
        issued_at = int(timestamp)
    except (TypeError, ValueError):
        return False
    current = int(time.time()) if now is None else now
    if abs(current - issued_at) > max_skew_seconds:
        return False
    expected = sign_request(secret, method, path, timestamp, body)
    return hmac.compare_digest(expected, signature)


@dataclass
class SlidingWindowLimiter:
    limit: int = 60
    window_seconds: int = 60
    _events: dict[str, list[int]] = field(default_factory=dict)

    def allow(self, client_id: str, now: int | None = None) -> bool:
        if not client_id:
            return False
        current = int(time.time()) if now is None else now
        events = [event for event in self._events.get(client_id, []) if current - event < self.window_seconds]
        if len(events) >= self.limit:
            self._events[client_id] = events
            return False
        events.append(current)
        self._events[client_id] = events
        return True


def validate_headers(headers: Mapping[str, str]) -> tuple[str, str, str] | None:
    """Extract required gateway headers without logging their values."""
    client_id = headers.get("x-fox-client-id", "").strip()
    timestamp = headers.get("x-fox-timestamp", "").strip()
    signature = headers.get("x-fox-signature", "").strip()
    if not client_id or not timestamp or not signature:
        return None
    return client_id, timestamp, signature
