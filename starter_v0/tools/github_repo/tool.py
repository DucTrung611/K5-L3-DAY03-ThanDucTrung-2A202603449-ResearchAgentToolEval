from __future__ import annotations

import os
from typing import Any

import requests

from tools._shared import TIMEOUT, err


def _clean_repo(repo: str) -> str:
    repo = (repo or "").strip()
    if "github.com/" in repo:
        repo = repo.split("github.com/")[-1]
    repo = repo.strip("/")
    parts = [p for p in repo.split("/") if p]
    if len(parts) >= 2:
        return f"{parts[0]}/{parts[1]}"
    return repo


def get_github_repo(repo: str = "") -> dict[str, Any]:
    try:
        clean_repo = _clean_repo(repo)
        if not clean_repo or "/" not in clean_repo:
            return {
                "tool": "get_github_repo",
                "error": "invalid_argument",
                "message": f"Expected repository in 'owner/repo' format, got: {repo!r}",
            }

        headers: dict[str, str] = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "ResearchAgent/1.0",
        }
        token = os.getenv("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"token {token}"

        url = f"https://api.github.com/repos/{clean_repo}"
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()

        return {
            "tool": "get_github_repo",
            "repo": clean_repo,
            "full_name": data.get("full_name", clean_repo),
            "description": data.get("description") or "",
            "stars": data.get("stargazers_count", 0),
            "forks": data.get("forks_count", 0),
            "language": data.get("language") or "Unknown",
            "url": data.get("html_url", f"https://github.com/{clean_repo}"),
            "open_issues": data.get("open_issues_count", 0),
        }
    except Exception as exc:
        return err("get_github_repo", exc)
