---
name: youtube_transcript
track: bonus
kind: live_api
provider: YouTube
requires_env: []
inputs: [url]
outputs: [video_id, url, title, transcript, items]
side_effect: false
---
# youtube_transcript

Extracts video ID and fetches English/Vietnamese transcripts or captions from a YouTube video URL.
Dùng khi người dùng đưa link video YouTube (`youtube.com` hoặc `youtu.be`) và yêu cầu đọc nội dung, tóm tắt video.