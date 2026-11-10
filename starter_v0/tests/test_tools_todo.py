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
    result = TOOL_FUNCTIONS["clarify"](question="Chọn một?", response_type="choice", options=["A", "B"])
    assert result["options"] == ["A", "B"]
    assert result["response_type"] == "choice"
    assert result["awaiting_user"] is True


# ---------------- format ----------------

def test_format_sections_groups_items_by_section() -> None:
    # Items with section "A", "B", "A" -> markdown has exactly one "## A" and one "## B".
    items = [
        {"title": "Item A1", "section": "A", "url": "https://a.com/1"},
        {"title": "Item B1", "section": "B", "url": "https://b.com/1"},
        {"title": "Item A2", "section": "A", "url": "https://a.com/2"},
    ]
    result = TOOL_FUNCTIONS["format"](items=items, template="sections")
    markdown = result["markdown"]
    assert markdown.count("## A") == 1
    assert markdown.count("## B") == 1
    assert "Item A1" in markdown
    assert "Item B1" in markdown
    assert "Item A2" in markdown


def test_format_thread_numbers_items() -> None:
    # template="thread" -> lines start with "1/", "2/", ...
    items = [
        {"title": "First tweet", "url": "https://x.com/1"},
        {"title": "Second tweet", "url": "https://x.com/2"},
    ]
    result = TOOL_FUNCTIONS["format"](items=items, template="thread")
    markdown = result["markdown"]
    assert "1/ First tweet" in markdown
    assert "2/ Second tweet" in markdown


def test_format_empty_items_does_not_crash() -> None:
    # items=None and items=[] -> item_count == 0, no exception.
    result_none = TOOL_FUNCTIONS["format"](items=None)
    assert result_none["item_count"] == 0
    assert result_none["markdown"] == ""

    result_empty = TOOL_FUNCTIONS["format"](items=[])
    assert result_empty["item_count"] == 0
    assert result_empty["markdown"] == ""


# ---------------- send (guardrail) ----------------

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    # Set TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID, mock HTTP.
    # Assert: exactly one POST, URL contains the token, json has chat_id + text, status == "sent".
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "fake_bot_token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "-100123456789")
    calls = fake_http(FakeResponse({"ok": True, "result": {"message_id": 123}}))
    result = TOOL_FUNCTIONS["send"](text="Bản tin công nghệ", confirmed=True)

    assert len(calls) == 1
    assert "fake_bot_token" in calls[0]["url"]
    assert calls[0]["json"]["chat_id"] == "-100123456789"
    assert calls[0]["json"]["text"] == "Bản tin công nghệ"
    assert result["status"] == "sent"


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    calls = fake_http(FakeResponse({"ok": True}))
    result = TOOL_FUNCTIONS["send"](text="Bản tin công nghệ", confirmed=True)

    assert len(calls) == 0
    assert result["error"] == "RuntimeError"
    assert "Missing TELEGRAM_BOT_TOKEN" in result["message"]


# ---------------- lookup ----------------

def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TAVILY_API_KEY", "test-key")
    calls = fake_http(FakeResponse({"results": []}))
    result = TOOL_FUNCTIONS["lookup"](query="AI", timeframe=None)
    assert "time_range" not in calls[0]["json"]
    assert result["items"] == []


# ---------------- fetch ----------------

def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "fc-test-key")
    fake_payload = {
        "data": {
            "markdown": "# Article Content\nHello world",
            "metadata": {
                "title": "Sample Article",
                "sourceURL": "https://example.com/article"
            }
        }
    }
    calls = fake_http(FakeResponse(fake_payload))
    result = TOOL_FUNCTIONS["fetch"](url="https://example.com/article")

    assert calls[0]["url"] == "https://api.firecrawl.dev/v1/scrape"
    assert calls[0]["json"]["url"] == "https://example.com/article"
    assert result["tool"] == "read_url"
    assert len(result["items"]) == 1
    item = result["items"][0]
    assert item["title"] == "Sample Article"
    assert item["url"] == "https://example.com/article"
    assert item["source"] == "example.com"
    assert item["summary"] == "# Article Content\nHello world"


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "fc-test-key")
    long_markdown = "A" * 6000
    fake_payload = {
        "data": {
            "markdown": long_markdown,
            "metadata": {"title": "Long Post", "sourceURL": "https://example.com/long"}
        }
    }
    fake_http(FakeResponse(fake_payload))
    result = TOOL_FUNCTIONS["fetch"](url="https://example.com/long")

    assert len(result["items"][0]["summary"]) == 4000
    assert result["items"][0]["summary"] == "A" * 4000


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
    result = TOOL_FUNCTIONS["policy"](query="")
    assert result["tool"] == "search_company_policy"
    assert result["results"] == []


def test_policy_area_filter_only_returns_that_area() -> None:
    result = TOOL_FUNCTIONS["policy"](query="retention personal data", policy_area="data_privacy")
    assert result["policy_area"] == "data_privacy"
    assert len(result["results"]) > 0
    for hit in result["results"]:
        assert hit["policy_area"] == "data_privacy"


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    # One policy file contains a quoted line that tries to give the assistant orders.
    # Query that section (source_citation) and assert: that line is in untrusted_text, NOT in facts.
    result = TOOL_FUNCTIONS["policy"](query="Injection probe", policy_area="source_citation")
    assert len(result["results"]) > 0
    hit = result["results"][0]
    assert hit["section"] == "Injection probe"
    assert any("ignore" in u.lower() for u in hit["untrusted_text"])
    assert "ignore" not in hit["facts"]


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


# ---------------- calculator (DucTrung) ----------------

def test_calculator_compound_interest_happy_path() -> None:
    out = TOOL_FUNCTIONS["calculator"]("1200*1.08**5", precision=2)
    assert out["result"] == 1763.19
    assert "error" not in out


@pytest.mark.parametrize("expr", ["", "   ", None, 123, "import os", "__import__('os')", "abs"])
def test_calculator_bad_input_returns_error_dict(expr) -> None:
    out = TOOL_FUNCTIONS["calculator"](expr)
    assert "error" in out and "result" not in out


def test_calculator_failure_paths_do_not_raise() -> None:
    calc = TOOL_FUNCTIONS["calculator"]
    assert calc("1/0")["error"] == "division by zero"
    assert "error" in calc("2**99999")
    assert "error" in calc("1+1", precision=99)


# ---------------- sentiment_analyzer (Tuan Anh) ----------------

def test_sentiment_happy_path() -> None:
    result = TOOL_FUNCTIONS["sentiment_analyzer"](text="This breakthrough AI model is fantastic, innovative, and great!")
    assert result["status"] == "ok"
    assert result["sentiment"] == "positive"
    assert result["score"] > 0
    assert "fantastic" in result["details"]["positive_keywords"]


def test_sentiment_bad_input_from_model() -> None:
    # Empty string
    r1 = TOOL_FUNCTIONS["sentiment_analyzer"](text="")
    assert r1["status"] == "ok"
    assert r1["sentiment"] == "neutral"
    assert r1["score"] == 0.0

    # None or non-string
    r2 = TOOL_FUNCTIONS["sentiment_analyzer"](text=None)
    assert r2["status"] == "ok"
    assert r2["sentiment"] == "neutral"


def test_sentiment_negative_and_neutral_return_ok_dict() -> None:
    # Test negative sentiment and neutral sentiment
    neg = TOOL_FUNCTIONS["sentiment_analyzer"](text="The system had a terrible crash and massive data loss failure.")
    assert neg["status"] == "ok"
    assert neg["sentiment"] == "negative"
    assert neg["score"] < 0

    neutral = TOOL_FUNCTIONS["sentiment_analyzer"](text="The report was published yesterday afternoon.")
    assert neutral["status"] == "ok"
    assert neutral["sentiment"] == "neutral"
    assert neutral["score"] == 0.0


# ---------------- youtube_transcript ----------------

def test_youtube_transcript_happy_path(monkeypatch, fake_http) -> None:
    fake_http(FakeResponse({
        "title": "Machine Learning Explained",
        "transcript": "Welcome to this machine learning introductory video."
    }))
    result = TOOL_FUNCTIONS["youtube_transcript"](url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    assert result["tool"] == "youtube_transcript"
    assert result["video_id"] == "dQw4w9WgXcQ"
    assert result["title"] == "Machine Learning Explained"
    assert "machine learning introductory video" in result["transcript"]
    assert len(result["items"]) == 1


def test_youtube_transcript_bad_url_returns_error_dict() -> None:
    result = TOOL_FUNCTIONS["youtube_transcript"](url="https://notyoutube.com/article")
    assert result["tool"] == "youtube_transcript"
    assert result["error"] == "ValueError"
    assert "Could not extract video ID" in result["message"]


def test_youtube_transcript_http_error_returns_error_dict(monkeypatch, fake_http) -> None:
    fake_http(FakeResponse(status_code=404))
    result = TOOL_FUNCTIONS["youtube_transcript"](url="https://youtu.be/dQw4w9WgXcQ")
    assert result["tool"] == "youtube_transcript"
    assert result["error"] == "HTTPError"
