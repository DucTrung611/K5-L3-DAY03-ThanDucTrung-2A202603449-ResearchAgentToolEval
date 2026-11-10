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

        # Endpoint lấy transcript (mockable trong test qua requests.get)
        api_url = f"https://api.youtube-transcripts.com/v1/transcript?video_id={video_id}"
        response = requests.get(api_url, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()

        title = data.get("title") or f"YouTube Video ({video_id})"
        transcript = data.get("transcript") or ""
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