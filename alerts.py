"""Notification-only Discord payload builders."""
from __future__ import annotations


def partnership_embed(repo: str, url: str) -> dict:
    return {"allowed_mentions": {"parse": []}, "embeds": [{"title": "New ecosystem candidate", "description": f"Candidate project discovered for review: {repo}", "url": url, "color": 3447003, "footer": {"text": "Discovery only • no partnership approved"}}]}


def grant_embed(repo: str, amount_usd: str) -> dict:
    return {"allowed_mentions": {"parse": []}, "embeds": [{"title": "Developer grant proposal", "description": f"A grant proposal was created for review: {repo}", "color": 10181046, "fields": [{"name": "Proposed amount", "value": f"${amount_usd} USD"}, {"name": "Status", "value": "pending_review; no payout executed"}]}]}
