"""TODO(student): Tool Unit Test Challenge.

Each test below is a stub. Replace `pytest.skip(...)` with a real test.
Patterns to copy are in test_tools_examples.py. Fixtures are in conftest.py.

Rules:
- Offline only: mock HTTP with `fake_http`, set fake keys with `monkeypatch.setenv`.
- One behaviour per test. Name the test after the behaviour, not the function.
- Done = `pytest tests/ -v` shows 0 skipped, 0 failed.
"""
from __future__ import annotations

import pytest

from conftest import FakeResponse  # noqa: F401  (you will need it)
from tools import TOOL_FUNCTIONS  # noqa: F401

TODO = "TODO(student): implement this test"


# ---------------- clarify ----------------

def test_clarify_choice_returns_options_and_awaits_user() -> None:
    # Call clarify with response_type="choice" and 2 options.
    # Assert: options are returned unchanged, awaiting_user is True.
    pytest.skip(TODO)


# ---------------- format ----------------

def test_format_sections_groups_items_by_section() -> None:
    # Items with section "A", "B", "A" -> markdown has exactly one "## A" and one "## B".
    pytest.skip(TODO)


def test_format_thread_numbers_items() -> None:
    # template="thread" -> lines start with "1/", "2/", ...
    pytest.skip(TODO)


def test_format_empty_items_does_not_crash() -> None:
    # items=None and items=[] -> item_count == 0, no exception.
    pytest.skip(TODO)


# ---------------- send (guardrail) ----------------

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    # Set TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID, mock HTTP.
    # Assert: exactly one POST, URL contains the token, json has chat_id + text, status == "sent".
    pytest.skip(TODO)


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    pytest.skip(TODO)


# ---------------- lookup ----------------

def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    # timeframe=None -> request body has no "time_range" key.
    pytest.skip(TODO)


# ---------------- fetch ----------------

def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    # Mock {"data": {"markdown": "...", "metadata": {"title": "T", "sourceURL": "https://..."}}}
    # Assert title/url/source/summary in result["items"][0].
    pytest.skip(TODO)


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    pytest.skip(TODO)


# ---------------- timeline / social_search ----------------

def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    # Mock {"timeline": [...]} with 1 item missing tweet_id and 6 valid items, limit=3.
    # Assert 3 items, and each url looks like https://x.com/<handle>/status/<id>.
    monkeypatch.setenv("RAPIDAPI_KEY", "test-rapidapi-key")
    raw_tweets = [{"screen_name": "sama", "text": "Missing id"}]  # missing tweet_id
    for i in range(1, 7):
        raw_tweets.append({"screen_name": "sama", "tweet_id": f"id_{i}", "text": f"Tweet {i}"})

    fake_http(FakeResponse({"timeline": raw_tweets}))
    result = TOOL_FUNCTIONS["timeline"](screenname="sama", limit=3)

    assert result["tool"] == "get_user_tweets"
    assert result["screenname"] == "sama"
    assert len(result["items"]) == 3
    for i, item in enumerate(result["items"], start=1):
        assert item["url"] == f"https://x.com/sama/status/id_{i}"
        assert item["source"] == "@sama"


def test_social_search_passes_search_type(monkeypatch, fake_http) -> None:
    # Assert the request params carry the query and search_type ("Top" / "Latest").
    monkeypatch.setenv("RAPIDAPI_KEY", "test-rapidapi-key")
    calls = fake_http(FakeResponse({"timeline": [
        {"screen_name": "openai", "tweet_id": "123", "text": "GPT-5 announcement"}
    ]}))

    result = TOOL_FUNCTIONS["social_search"](query="GPT-5", search_type="Top", limit=2)

    assert calls[0]["url"] == "https://twitter-api45.p.rapidapi.com/search.php"
    assert calls[0]["params"]["query"] == "GPT-5"
    assert calls[0]["params"]["search_type"] == "Top"
    assert calls[0]["headers"]["x-rapidapi-key"] == "test-rapidapi-key"
    assert result["tool"] == "search_tweets"
    assert len(result["items"]) == 1


# ---------------- policy (local knowledge + trust boundary) ----------------

def test_policy_empty_query_returns_no_results() -> None:
    pytest.skip(TODO)


def test_policy_area_filter_only_returns_that_area() -> None:
    # policy_area="data_privacy" -> every result has policy_area == "data_privacy".
    pytest.skip(TODO)


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    # One policy file contains a quoted line that tries to give the assistant orders.
    # Query that section (source_citation) and assert: that line is in untrusted_text, NOT in facts.
    pytest.skip(TODO)


# ---------------- YOUR NEW TOOL(S) ----------------
# github_repo (Trần Mạnh Hùng)
def test_github_repo_happy_path(fake_http) -> None:
    calls = fake_http(FakeResponse({
        "full_name": "openai/whisper",
        "description": "Robust Speech Recognition via Large-Scale Weak Supervision",
        "stargazers_count": 80000,
        "forks_count": 10000,
        "language": "Python",
        "html_url": "https://github.com/openai/whisper",
        "open_issues_count": 500,
    }))

    result = TOOL_FUNCTIONS["github_repo"](repo="openai/whisper")

    assert calls[0]["url"] == "https://api.github.com/repos/openai/whisper"
    assert result["tool"] == "get_github_repo"
    assert result["repo"] == "openai/whisper"
    assert result["stars"] == 80000
    assert result["forks"] == 10000
    assert result["language"] == "Python"
    assert result["url"] == "https://github.com/openai/whisper"


def test_github_repo_bad_input_from_model() -> None:
    # Empty string or invalid format without slash
    result_empty = TOOL_FUNCTIONS["github_repo"](repo="")
    assert result_empty["error"] == "invalid_argument"

    result_no_slash = TOOL_FUNCTIONS["github_repo"](repo="invalid_name")
    assert result_no_slash["error"] == "invalid_argument"


def test_github_repo_failure_returns_error_dict(fake_http) -> None:
    # HTTP error (e.g. 404 repo not found) returns error dict without raising
    fake_http(FakeResponse(status_code=404))
    result = TOOL_FUNCTIONS["github_repo"](repo="nonexistent/repo")

    assert result["error"] == "HTTPError"
    assert result["tool"] == "get_github_repo"
