# Implementation Plan — RAG Pipeline Lab

## 👥 Phân công nhiệm vụ (Roles)

| Vai trò | Trách nhiệm chính | Sprint lead |
|---------|------------------|------------|
| **Tech Lead** | Giữ nhịp sprint, nối code end-to-end | 1, 2 |
| **Retrieval Owner** | Chunking, metadata, retrieval strategy, rerank | 1, 3 |
| **Eval Owner** | Test questions, expected evidence, scorecard, A/B | 3, 4 |
| **Documentation Owner** | architecture.md, tuning-log, báo cáo nhóm | 4 |

---

## 🟢 Sprint 1: Build Index (DONE)
- [x] Implement `get_embedding()` using Jina AI API.
- [x] Implement `build_index()` with ChromaDB.
- [x] Extract metadata: `source`, `section`, `department`, `effective_date`, `access`.
- [x] Implement paragraph-based chunking.
- [x] Verify index with `list_chunks()` and `inspect_metadata_coverage()`.

---

## 🔵 Sprint 2: Baseline Retrieval + Answer (DONE)
**File:** `rag_answer.py`

### Tasks:
1. **Implement `retrieve_dense()`**:
   - [x] Chuyển câu hỏi (query) thành vector bằng Jina model (`retrieval.query`).
   - [x] Tìm kiếm `top_k` chunk từ ChromaDB collection `rag_lab`.
   - [x] Trả về danh sách chunk kèm `score`.
2. **Implement `call_llm()`**:
   - [x] Sử dụng OpenAI (GPT-4o-mini).
   - [x] Cấu hình `temperature=0` để đảm bảo kết quả ổn định.
3. **Thực thi `rag_answer()`**:
   - [x] Kết hợp Retrieval -> Context Prompt -> LLM.
   - [x] Thử nghiệm với các câu hỏi mẫu (SLA, Hoàn tiền, Abstain).

### Definition of Done (DOD):
- [x] Trả lời đúng có kèm Citation (Ví dụ: `[1]`).
- [x] Nếu không có dữ liệu, trả về "Tôi không đủ thông tin để trả lời".
- [x] Trình bày rõ ràng các `sources` đã tìm được.

---

## 🟡 Sprint 3: Tuning & Optimization (DONE)
**File:** `rag_answer.py`

### Lựa chọn Variant:
Dựa trên bối cảnh dữ liệu (có mã lỗi, từ khóa kỹ thuật), chúng ta đã triển khai **Hybrid + Rerank**.

### Tasks:
1. **Tuning Retrieval**:
   - [x] **Option Hybrid**: Implement BM25 (sparse) kết hợp với Vector (dense).
   - [x] **Option Rerank**: Dùng Jina Reranker để sắp xếp lại kết quả.
2. **Evaluation Sơ bộ**:
   - [x] Dùng hàm `compare_retrieval_strategies()` để so sánh Baseline vs Variant.
3. **Logging**:
   - [x] Ghi lại các thay đổi và kết quả thí nghiệm vào `docs/tuning-log.md`.

---

## 🔴 Sprint 4: Evaluation, Documentation & Final Report
**File:** `eval.py` & `docs/` & `reports/`

### Tasks:
1. **Chấm điểm (Evaluation)**:
   - Sử dụng bộ 10 câu hỏi trong `data/test_questions.json`.
   - Thực hiện chấm điểm qua `eval.py` để tính các chỉ số: `Faithfulness`, `Answer Relevance`, `Context Recall`.
   - **Bonus (+2)**: Implement LLM-as-Judge để tự động hóa việc chấm điểm.
2. **So sánh A/B (A/B Testing)**:
   - Chạy `run_scorecard(BASELINE_CONFIG)` và `run_scorecard(VARIANT_CONFIG)`.
   - Sử dụng `compare_ab()` để phân tích sự khác biệt (delta) giữa bản gốc và bản đã tối ưu.
3. **Hoàn thiện Tài liệu (Documentation)**:
   - `docs/architecture.md`: Vẽ sơ đồ pipeline và giải thích chiến lược chunking.
   - `docs/tuning-log.md`: Ghi lại kết quả thí nghiệm và lý do chọn giải pháp tối ưu.
4. **Báo cáo cá nhân (Individual Reports)**:
   - Viết bài phân tích (500-800 từ) về phần việc mình đảm nhận và rút kinh nghiệm thực tế.

### Definition of Done (DOD):
- [ ] Demo chạy trơn tru: `python index.py && python rag_answer.py && python eval.py`.
- [ ] Báo cáo nhóm và báo cáo cá nhân đầy đủ trong thư mục `reports/`.
- [ ] Log chạy grading (`logs/grading_run.json`) sẵn sàng trước 18:00.
