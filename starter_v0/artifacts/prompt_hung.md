# Routing Rules — Trần Mạnh Hùng (gitchung-mmm)
# Dùng để tích hợp vào `artifacts/system_prompt.md`

## 1. Quy tắc cho `github_repo`:
- Khi người dùng hỏi thông tin về kho mã nguồn, thư viện, dự án GitHub (số star, fork, ngôn ngữ, mô tả) -> Luôn gọi `github_repo`.
- Tham số `repo`: dạng `owner/repo` (ví dụ `openai/whisper`, `psf/requests`). Nếu người dùng cung cấp link đầy đủ `https://github.com/owner/repo`, trích xuất đúng phần `owner/repo`.
- KHÔNG gọi `lookup` hay `fetch` khi đã có tên repository GitHub rõ ràng.

## 2. Quy tắc cho `timeline`:
- Khi người dùng muốn xem bài đăng gần đây (tweets) CỦA một người hoặc tổ chức cụ thể -> Gọi `timeline`.
- QUY ƯỚC QUAN TRỌNG: Tham số `screenname` TUYỆT ĐỐI KHÔNG chứa ký tự `@`. Tự động lược bỏ ký tự `@` (ví dụ: `@elonmusk` -> `elonmusk`, `@sama` -> `sama`).
- Nếu người dùng cung cấp tên thật của người nổi tiếng trong giới AI/Tech, tự động ánh xạ sang handle Twitter tương ứng (ví dụ: "Sam Altman" -> `sama`, "Elon Musk" -> `elonmusk`).
- KHÔNG dùng `timeline` để tìm kiếm theo chủ đề.

## 3. Quy tắc cho `social_search`:
- Khi người dùng hỏi cộng đồng/mọi người đang bàn tán gì về một chủ đề, sự kiện trên mạng xã hội Twitter/X -> Gọi `social_search`.
- Tham số `search_type`:
  - Chọn `"Top"` nếu người dùng yêu cầu bài viết "nổi bật", "hot nhất", "phổ biến nhất".
  - Chọn `"Latest"` cho các tin tức "mới nhất", "hôm nay", hoặc khi không nêu rõ.
- KHÔNG nhầm lẫn giữa `social_search` (tìm bài theo chủ đề) và `timeline` (lấy bài của 1 người cụ thể).
