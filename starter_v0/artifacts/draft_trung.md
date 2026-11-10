# Nháp của DucTrung (calculator + lookup + clarify)

Dán các đoạn dưới vào `system_prompt.md` khi gộp. Mỗi version chỉ thêm MỘT giả thuyết.

## Prompt rule

### calculator
- Khi người dùng cần ra một con số (lãi suất, phần trăm, trung bình, tổng, quy đổi), luôn gọi `calculator`, không tự nhẩm. Truyền `expression` là biểu thức thuần số; nếu người dùng nêu số chữ số thập phân thì truyền `precision`.
- Không dùng `calculator` cho dữ liệu cần tra cứu (giá, tỷ giá, số liệu hiện tại): dùng `lookup` lấy số trước, rồi mới gọi `calculator` nếu cần tính tiếp.

### clarify
- Thiếu thông tin bắt buộc (ví dụ không nói tweet của ai, "bài viết này" mà không có URL): gọi `clarify` để hỏi, tuyệt đối không đoán một người hay một URL.

### lookup
- Dùng `lookup` cho tin tức, sự kiện, số liệu trên web. Không dùng khi người dùng muốn tweet của một tài khoản (dùng `timeline`) hoặc chỉ cần tính toán (dùng `calculator`).

## Gợi ý thứ tự đo
- v1: thêm rule `clarify` (nhắm R10, R11 đang fail missing_info).
- v2: thêm rule `calculator` + ranh giới `lookup`.
- v3: gộp rule của cả nhóm, sửa phần "hate being asked questions" và "just go ahead and send".

## Schema YAML
Đã khai báo `calculator` ở cuối `artifacts/tools.yaml`. Còn việc viết lại mô tả `clarify` và `lookup`
(công dụng, khi nào dùng, khi nào KHÔNG dùng) khi gộp v1/v2.
