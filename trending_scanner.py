"""Daily read-only discovery scanner for AI and agent projects on GitHub."""
from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

QUERIES = {
    "artificial-intelligence": "topic:artificial-intelligence archived:false",
    "agents": "(topic:agents OR topic:llm-agents OR topic:autonomous-agents) archived:false",
    "research": "(topic:research OR topic:developer-tools) archived:false",
}


def github_get(path: str) -> dict:
    url = "https://api.github.com" + path
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "handasa-ecosystem-hub"}
    token = os.environ.get("GITHUB_READ_TOKEN", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=20) as response:  # nosec B310: fixed https API host
        return json.loads(response.read().decode())


def scan(per_query: int = 10) -> dict:
    projects = []
    for category, query in QUERIES.items():
        params = urllib.parse.urlencode({"q": query, "sort": "stars", "order": "desc", "per_page": per_query})
        data = github_get(f"/search/repositories?{params}")
        for item in data.get("items", []):
            projects.append({"category": category, "full_name": item["full_name"], "url": item["html_url"],
                             "description": item.get("description") or "", "stars": item.get("stargazers_count", 0),
                             "forks": item.get("forks_count", 0), "language": item.get("language"),
                             "pushed_at": item.get("pushed_at"), "license": (item.get("license") or {}).get("spdx_id")})
    unique = {project["full_name"]: project for project in projects}
    return {"scanned_at": datetime.now(timezone.utc).isoformat(), "source": "GitHub public repository search API", "projects": sorted(unique.values(), key=lambda row: row["stars"], reverse=True)}


def main() -> int:
    try:
        result = scan(int(os.environ.get("RESULTS_PER_QUERY", "10")))
        output = Path(os.environ.get("TRENDING_OUTPUT", "reports/trending.json"))
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except Exception as exc:
        print(f"Trending scan failed closed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
