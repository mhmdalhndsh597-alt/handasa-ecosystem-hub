"""Grant proposal calculator with mandatory human review.

It creates allocation proposals only. No payout, wallet access, signing, or transfer is implemented.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path


def build_grant(project: dict, amount_usd: Decimal, milestones: list[str]) -> dict:
    if amount_usd <= 0 or not milestones:
        raise ValueError("grant amount and milestones must be positive/non-empty")
    return {"project": project, "amount_usd": str(amount_usd), "milestones": milestones,
            "status": "pending_review", "payout_enabled": False, "requires_multisig_approval": True,
            "created_at": datetime.now(timezone.utc).isoformat()}


def build_configuration_notice(project: dict) -> dict:
    """Return a non-funding report when the optional grant amount is not configured."""
    return {
        "project": project,
        "amount_usd": None,
        "milestones": [],
        "status": "awaiting_configuration",
        "payout_enabled": False,
        "requires_multisig_approval": True,
        "reason": "GRANT_AMOUNT_USD is not configured; no grant proposal was created",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def main() -> int:
    try:
        project = json.loads(Path(os.environ.get("GRANT_PROJECT_FILE", "grant.example.json")).read_text())
        raw_amount = os.environ.get("GRANT_AMOUNT_USD", "").strip()
        proposal = (
            build_configuration_notice(project)
            if not raw_amount
            else build_grant(project, Decimal(raw_amount), ["technical due diligence", "public milestone report", "security review"])
        )
        output = Path(os.environ.get("GRANT_OUTPUT", "reports/grant-proposal.json"))
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(proposal, indent=2, ensure_ascii=False) + "\n")
        print(json.dumps(proposal, indent=2, ensure_ascii=False))
        return 0
    except Exception as exc:
        print(f"Grant proposal failed closed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
