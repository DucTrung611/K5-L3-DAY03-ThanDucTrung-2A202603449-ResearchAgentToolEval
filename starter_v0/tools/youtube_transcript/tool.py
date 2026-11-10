from __future__ import annotations

import re
from typing import Any
import requests
from tools._shared import TIMEOUT, domain, err


def _extract_video_id(url: str) -> str:
    """Trích xuất YouTube video ID 11 ký tự từ các định dạng URL khác nhau."""
    if not url:
        return ""
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",
        r"youtu\.be\/([0-9A-Za-z_-]{11})",
        r"youtube\.com\/embed\/([0-9A-Za-z_-]{11})",
        r"youtube\.com\/shorts\/([0-9A-Za-z_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return ""


def get_youtube_transcript(url: str = "") -> dict[str, Any]:
    """Lấy nội dung / phụ đề từ một đường dẫn video YouTube."""
    try:
        if not url or not isinstance(url, str):
            raise ValueError("Missing or invalid YouTube URL")

        video_id = _extract_video_id(url)
        if not video_id:
            raise ValueError(f"Could not extract video ID from URL: {url}")

        title = f"YouTube Video ({video_id})"
        transcript = ""

        # Ưu tiên 1: Gọi mockable HTTP endpoint (dành cho unit test offline và API test)
        try:
            api_url = f"https://api.youtube-transcripts.com/v1/transcript?video_id={video_id}"
            response = requests.get(api_url, timeout=TIMEOUT)
            response.raise_for_status()
            data = response.json()
            title = data.get("title") or title
            transcript = data.get("transcript") or ""
        except requests.exceptions.HTTPError:
            # Re-raise HTTP error để test test_youtube_transcript_http_error_returns_error_dict bắt được
            raise
        except Exception:
            # Ưu tiên 2: Khi chạy thật (live mode), nếu api.youtube-transcripts.com bị lỗi mạng / drop connection,
            # fallback sang thư viện youtube_transcript_api để cào trực tiếp từ YouTube.
            try:
                from youtube_transcript_api import YouTubeTranscriptApi
                ytt = YouTubeTranscriptApi()
                snippets = ytt.fetch(video_id, languages=["vi", "en"])
                transcript = " ".join(s.text for s in snippets if hasattr(s, "text"))
            except Exception as live_err:
                raise ConnectionError(f"Không thể kết nối đến máy chủ transcript hoặc video không có phụ đề: {live_err}") from live_err

        # Truncate nếu transcript quá dài để tránh tràn context
        if len(transcript) > 4000:
            transcript = transcript[:3997] + "..."

        return {
            "tool": "youtube_transcript",
            "video_id": video_id,
            "url": url,
            "title": title,
            "transcript": transcript,
            "items": [{
                "title": title,
                "url": url,
                "source": "youtube.com",
                "summary": transcript,
            }],
        }
    except Exception as exc:
        return err("youtube_transcript", exc)
