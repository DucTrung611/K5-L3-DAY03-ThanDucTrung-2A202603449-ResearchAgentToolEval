---
name: github_repo
track: bonus
kind: live_api
provider: GitHub
requires_env: []
inputs: [repo]
outputs: [tool, repo, full_name, description, stars, forks, language, url, open_issues]
side_effect: false
---
# github_repo

Tra cứu thông tin chi tiết của một kho lưu trữ (repository) trên GitHub: số stars, forks, ngôn ngữ lập trình, mô tả dự án và URL chính thức.
Tham số đầu vào: `repo` có thể là định dạng `owner/repo` (ví dụ `openai/whisper`) hoặc đường link GitHub đầy đủ.
