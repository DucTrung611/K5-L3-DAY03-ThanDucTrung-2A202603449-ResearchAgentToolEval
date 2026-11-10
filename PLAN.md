# Phân công nhóm — Day 03 Research Agent Tool Eval

Nhóm trưởng: **DucTrung611**. Thành viên: **Trần Mạnh Hùng (gitchung-mmm)**, **khackhanh1201**, **phamtuananhhatay**.

## Nguyên tắc

- Vòng tối ưu v0 → v1 → v2 → v3 phải tuần tự (mỗi version dựa trên kết quả version trước), nên chỉ **một người** làm: nhóm trưởng.
- Tool mới, unit test, eval case và UI độc lập nhau, nên làm song song.
- Mỗi file có **một chủ sở hữu** để không conflict git (xem bảng cuối).
- Mỗi người làm trên nhánh riêng `feat/<tên>`, mở PR về `main`, nhóm trưởng review và merge.
- Không commit `.env`. Key chia riêng qua kênh nhóm.

## Phân công

### 1. DucTrung611 — Tối ưu prompt/tools + tích hợp
- Setup `.env` (provider key, `TAVILY_API_KEY`, `FIRECRAWL_API_KEY`, `RAPIDAPI_KEY`), chạy `python scripts/preflight_provider.py --provider openrouter`.
- Chạy baseline `v0`, liệt kê case FAIL và gán `failure_type`.
- Sửa `artifacts/system_prompt.md`:
  - bỏ chỉ dẫn xấu của starter (đoán thay vì hỏi, gửi không xác nhận, ép một bước)
  - thêm rule routing cho `timeline` / `social_search` / `lookup` / `fetch` / `clarify`
- Sửa `artifacts/tools.yaml`:
  - `description` mỗi tool nêu khi nào dùng / khi nào không dùng
  - quy ước args: handle không có `@`, `topic=news`, `timeframe`, `search_type=Top|Latest`
  - `send` chỉ gửi khi `confirmed=true`
- Chạy v1, v2, v3, mỗi version một giả thuyết, điền `artifacts/version_log.csv`.
- Viết REPORT **B1, B2, B6**. Review và merge PR.
- **Nộp:** `version_log.csv`, `runs/*.json`, B1/B2/B6.

### 2. Trần Mạnh Hùng (gitchung-mmm) — Tool mới + test cho tool mới
- Viết **≥ 4 tool mới** (bonus yêu cầu "hơn 3 tool"). Mỗi tool gồm `tools/<tên>/tool.py` và `TOOL.md` đúng contract trong `tools/README.md`.
- Đăng ký trong `tools/__init__.py` (`TOOL_FUNCTIONS`). Gửi entry `tools.yaml` cho nhóm trưởng để gộp.
- Viết **≥ 3 test mỗi tool mới** (happy path; input xấu như chuỗi rỗng, sai kiểu, ngoài enum; nhánh lỗi trả error dict, không raise) trong mục "YOUR NEW TOOL(S)" của `tests/test_tools_todo.py`.
- **Việc đầu tiên:** chốt tên 4 tool trong vòng 1 giờ và báo nhóm (khackhanh1201 cần tên để viết eval case).
- **Nộp:** 4 thư mục tool, test xanh, mô tả tool cho REPORT A2.

### 3. khackhanh1201 — Unit test tool có sẵn + eval case nhóm
- Điền **17 stub** `pytest.skip(TODO)` trong `tests/test_tools_todo.py` (clarify, format, send, lookup, fetch, timeline, social_search, policy). Mục tiêu: `pytest` **0 failed, 0 skipped**.
- Challenge+: thử input biên (`limit=0`, `top_k=0`, `max_results="5"`, `items` thiếu `url`). Nếu tìm được bug: sửa, giữ test làm regression, ghi vào REPORT **B5**.
- Viết **10 eval case** vào `data/eval_group.json` (5 single-turn, 5 multi-turn). Mỗi case cần `id`, `phase: "B"`, `query` hoặc `turns`, `failure_type`, `expect`, `metadata.what_it_tests`.
  - Phủ các loại lỗi: `wrong_tool`, `wrong_arg_value`, `wrong_boundary`, `unnecessary_tool`, `out_of_scope`, `missing_info`.
  - Có ≥ 1 case route tới mỗi tool mới của Hùng.
- Sau khi có v3, chạy suite `group`, viết REPORT **B3**.
- **Nộp:** `test_tools_todo.py` (phần tool có sẵn), `eval_group.json`, B3, phần "Tool unit tests" trong B5.

### 4. phamtuananhhatay — UI + demo + REPORT Phần A
- Dựng **UI Streamlit** (`app.py`) bọc `agent.py`/`chat.py`: ô chat, hiển thị tool calls, bước xác nhận trước khi `send`. UI là bắt buộc, và cùng ≥ 4 tool mới là điều kiện lấy điểm thưởng.
- Deploy bằng Cloudflare Tunnel (xem README), dán link vào REPORT A1.
- Viết REPORT **Phần A (A1–A3)**, có thể thêm `artifacts/poster.html`. **Hạn: trước 16:30.**
- Chạy `python chat.py --provider openrouter --version v3` ≥ 3 lượt live: request bình thường; request thiếu thông tin rồi bổ sung; request "gửi lên Telegram". Lưu transcript, viết **B4**.
- **Nộp:** `app.py`, link demo, poster, Phần A, B4, `transcripts/*.json`.

### Bonus (tuỳ chọn, chỉ làm khi v3 đã ổn)
- **Small Local Model (Ollama, Step 7)**: phamtuananhhatay sau khi xong UI, hoặc khackhanh1201 sau khi xong test. Ghi vào B7.
- **`send` có transcript chứng minh xác nhận**: làm chung khi chạy live chat.

## Mốc giờ theo lịch lớp (ca 14:00–18:00)

Lấy từ slide tiến độ của lớp. Giờ đã co theo tỉ lệ (14:00–14:15 ổn định lớp, lab chạy 14:15–18:00). Ca khác thì dịch theo giờ bắt đầu của ca.

| Giờ | Mốc | Trưởng | Hùng | khackhanh1201 | phamtuananhhatay |
|---|---|---|---|---|---|
| 14:15–14:35 | Setup | Lấy key, preflight, chia key | Cài môi trường, đọc `tools/README.md`, chốt tên 4 tool | Cài môi trường, chạy `pytest` | Cài môi trường, khởi tạo `app.py` |
| 14:35–15:10 | Baseline v0 + dựng UI | Chạy v0, phân loại lỗi, ghi `version_log.csv` | Viết tool #1, #2 | Điền stub test: clarify, format, send | UI Streamlit chạy được ở `localhost:8501` |
| 15:10–15:40 | v1 + ≥ 1 tool mới | Sửa prompt/tools, chạy v1 | Tool #1 qua contract test, đăng ký `tools.yaml` | Stub test: lookup, fetch | UI hiển thị tool calls |
| 15:40–16:10 | Team eval + v2 | Chạy v2 + suite `group` | Tool #3, #4 + ≥ 3 test mỗi tool | 10 eval case vào `eval_group.json` | UI có bước xác nhận trước `send` |
| **16:10–16:35** | **REPORT Phần A + link demo** (**cứng: trước 16:30**) | Duyệt Phần A | Gửi mô tả tool cho A2 | Hỗ trợ câu hỏi mẫu A3 | Viết Phần A, chạy Cloudflare Tunnel, dán link |
| 16:35–17:30 | Team showdown | Demo, ghi lỗi quan sát được | Thử agent của team khác | Thử agent của team khác | Giữ UI + tunnel chạy suốt buổi |
| 17:30–18:00 | v3 + REPORT Phần B + nộp | Chạy v3 từ lỗi showdown, B1/B2/B6 | Hoàn thiện test tool mới | Chạy suite `group` với v3, B3, B5 | `chat.py` ≥ 3 lượt, B4, transcript |

Các mốc cứng:
- Cuối 15:40: có ≥ 1 tool mới qua `pytest tests/test_tool_contract.py`.
- 16:30: Phần A xong và có link demo.
- v3 dùng lỗi quan sát được ở showdown làm giả thuyết (ghi lại câu hỏi làm agent sai, đưa thành eval case mới).

## Nộp bài và deadline

- **Deadline**: ca 9:00 và ca 14:00 là 23:59 cùng ngày; ca 16:30 là 12:00 trưa hôm sau (trừ khi giảng viên báo khác). **Nộp muộn bị trừ điểm.**
- **Web nộp**: `aithucchien.vinuni.edu.vn`, đăng nhập LMS, vào bài Day 03, dán link repo.
- **Cả nhóm làm trên một repo duy nhất**: repo của DucTrung611 (`K5-L3-DAY03-ThanDucTrung-2A202603449-ResearchAgentToolEval`). Giữ nguyên tên repo, không tạo repo mới. 3 thành viên đã là Collaborator nên clone về và đẩy nhánh `feat/<tên>`.
- **Liệt kê 4 thành viên trong `TEAM.md`** ở thư mục gốc repo (DucTrung611 tạo file này ở giai đoạn setup).
- **Nộp bài**: cả 4 người dán cùng link repo này lên LMS.
- Repo không chứa `.env` hay API key.
- **Điểm danh**: quét QR khi vào lớp **và** cuối buổi.

## API key cần có

Trưởng nhóm điền vào `starter_v0/.env`, chia cho các bạn qua kênh riêng:

| Biến | Dùng cho |
|---|---|
| `OPENROUTER_API_KEY` | Model (bắt buộc) |
| `TAVILY_API_KEY` | tool `lookup` |
| `FIRECRAWL_API_KEY` | tool `fetch` |
| `RAPIDAPI_KEY` | tool `timeline`, `social_search` (subscribe gói BASIC $0 của Twitter45) |
| `TELEGRAM_BOT_TOKEN` | tool `send` (bonus), tạo bot qua @BotFather và thêm bot làm admin channel |

Nếu kẹt key quá 10 phút, chạy chung máy của nhóm khác, đừng để cả nhóm đứng chờ.

## Chủ sở hữu file

| File | Chủ sở hữu | Người khác muốn sửa thì |
|---|---|---|
| `artifacts/system_prompt.md`, `artifacts/tools.yaml`, `artifacts/version_log.csv` | DucTrung611 | Gửi đề xuất cho trưởng |
| `tools/<tool mới>/`, `tools/__init__.py` | Hùng | |
| `tests/test_tools_todo.py` | khackhanh1201 (mục YOUR NEW TOOL: Hùng) | Hùng chỉ sửa trong mục YOUR NEW TOOL |
| `data/eval_group.json` | khackhanh1201 | |
| `app.py`, `artifacts/poster.html`, REPORT Phần A | phamtuananhhatay | |
| REPORT Phần B | Mỗi người một mục: B1/B2/B6 trưởng, B3 + B5 (test) khackhanh1201, B4 phamtuananhhatay | |

## Quy trình làm việc chung (git)

Mọi lệnh chạy trong `starter_v0/` sau khi clone repo của DucTrung611.

1. `git checkout -b feat/<tên>` (tạo nhánh riêng, không commit trực tiếp lên `main`).
2. Làm xong một phần nhỏ thì `pytest`, rồi `git add <file>`, `git commit`, `git push -u origin feat/<tên>`.
3. Mở PR về `main`, báo trưởng nhóm. Trưởng nhóm review và merge.
4. Trước khi làm tiếp: `git checkout main && git pull`, rồi `git checkout feat/<tên> && git merge main`.
5. Chỉ sửa file thuộc phần mình (xem bảng chủ sở hữu file). Cần sửa file người khác thì nhắn họ.

## Workflow từng người

### DucTrung611 (trưởng nhóm)
1. Tạo `TEAM.md`, điền `.env`, chạy `preflight_provider.py`, chia key cho các bạn.
2. Chạy v0: `python run_eval.py --provider openrouter --version v0 --suite base --eval-cases data/eval_base.json`.
3. Mở `runs/*.json`, liệt kê case FAIL và gán `failure_type`; ghi dòng v0 vào `version_log.csv`.
4. Đặt một giả thuyết, sửa `system_prompt.md` hoặc `tools.yaml`, chạy v1, ghi version log. Lặp lại cho v2, v3.
5. Gộp entry `tools.yaml` của Hùng, chạy `pytest tests/test_tool_contract.py`.
6. Review và merge PR của cả nhóm (ưu tiên PR của Hùng và phamtuananhhatay).
7. Sau showdown: ghi lỗi quan sát được, đưa cho khackhanh1201 làm eval case, chạy v3.
8. Viết REPORT B1, B2, B6, kiểm tra repo không có `.env`, nộp link lên LMS.

### Trần Mạnh Hùng
1. Đọc `tools/README.md` và 2 tool mẫu (ví dụ `tools/lookup/`), chốt tên 4 tool, báo nhóm.
2. Mỗi tool: tạo `tools/<tên>/tool.py` và `TOOL.md`, đăng ký trong `tools/__init__.py`.
3. Chạy `pytest tests/test_tool_contract.py` cho đến khi xanh.
4. Gửi entry `tools.yaml` cho trưởng nhóm (không tự sửa file).
5. Viết ≥ 3 test mỗi tool trong `tests/test_tools_todo.py`, mục YOUR NEW TOOL(S): happy path, input xấu, nhánh lỗi.
6. Mở PR sau mỗi tool để trưởng nhóm merge sớm, không dồn đến cuối.
7. Gửi mô tả từng tool cho phamtuananhhatay (REPORT A2).

### khackhanh1201
1. Chạy `pytest -v`, nhận diện 17 stub `pytest.skip(TODO)` trong `tests/test_tools_todo.py`.
2. Điền stub theo thứ tự: clarify, format, send, lookup, fetch, timeline, social_search, policy (mẫu ở `tests/test_tools_examples.py`, mock HTTP bằng `fake_http`).
3. Thử input biên (`limit=0`, `max_results="5"`, `items` thiếu `url`); nếu tìm được bug thì sửa, giữ test làm regression, ghi lại cho B5.
4. Khi Hùng chốt tên tool: viết 10 case vào `data/eval_group.json` (5 single, 5 multi), có ≥ 1 case mỗi tool mới.
5. Sau khi có v3: chạy `--suite group` và viết REPORT B3, B5.
6. Sau showdown: thêm eval case từ lỗi thật của các team.

### phamtuananhhatay
1. Đọc `agent.py` và `chat.py`, tạo `app.py` Streamlit (ô chat, hiển thị tool calls, lịch sử).
2. Thêm bước xác nhận trước khi gọi `send` (`confirmed=true` chỉ khi user bấm xác nhận).
3. Chạy `streamlit run app.py` và `cloudflared tunnel --url http://localhost:8501`, dán link vào REPORT A1.
4. Viết REPORT Phần A (A1–A3) trước 16:30, tuỳ chọn thêm `artifacts/poster.html`.
5. Giữ UI và tunnel chạy suốt showdown.
6. Chạy `python chat.py --provider openrouter --version v3` ≥ 3 lượt (bình thường, thiếu thông tin rồi bổ sung, gửi Telegram), lưu transcript và viết B4.

## Lưu ý

- **Không đổi tên tool có sẵn.** Nếu cần, phải đồng bộ `tools.yaml`, `tools/__init__.py`, `eval_base.json`, `eval_research_extension.json` (xem README).
- Không sửa nội dung case trong `data/eval_base.json`.
- `pytest` phải xanh trước khi mở PR (`test_tool_contract.py` luôn phải pass).
- Hạn 16:30 chỉ áp dụng cho Phần A. Phần B hoàn thiện sau showdown để nộp.
- Mỗi version chỉ đổi **một giả thuyết**; số liệu trong REPORT phải khớp `runs/*.json`, không ghi theo cảm giác.
- Link Cloudflare Tunnel sống theo phiên lệnh: tắt terminal là mất link, nên giữ `streamlit run app.py` và `cloudflared tunnel --url http://localhost:8501` chạy suốt showdown.
