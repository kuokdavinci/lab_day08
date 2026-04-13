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

## 🔵 Sprint 2: Baseline Retrieval + Answer (Current)
**File:** `rag_answer.py`

### Tasks:
1. **Implement `retrieve_dense()`**:
   - Chuyển câu hỏi (query) thành vector bằng Jina model (`retrieval.query`).
   - Tìm kiếm `top_k` chunk từ ChromaDB collection `rag_lab`.
   - Trả về danh sách chunk kèm `score`.
2. **Implement `call_llm()`**:
   - Sử dụng OpenAI (GPT-4o-mini) hoặc Google Gemini.
   - Cấu hình `temperature=0` để đảm bảo kết quả ổn định.
3. **Thực thi `rag_answer()`**:
   - Kết hợp Retrieval -> Context Prompt -> LLM.
   - Thử nghiệm với các câu hỏi mẫu:
     - *"SLA xử lý ticket P1 là bao lâu?"*
     - *"Khách hàng có thể yêu cầu hoàn tiền trong bao nhiêu ngày?"*
     - *"Dữ liệu rác/Không có trong tài liệu"* (Test khả năng "abstain" - từ chối trả lời).

### Definition of Done (DOD):
- [ ] Trả lời đúng có kèm Citation (Ví dụ: `[1]`).
- [ ] Nếu không có dữ liệu, trả về "Tôi không đủ thông tin để trả lời".
- [ ] Trình bày rõ ràng các `sources` đã tìm được.

---

## 🟡 Sprint 3: Tuning & Optimization
**File:** `rag_answer.py`

### Lựa chọn Variant:
Dựa trên bối cảnh dữ liệu (có mã lỗi, từ khóa kỹ thuật), chúng ta sẽ chọn **Variant: Hybrid Search** hoặc **Rerank**.

### Tasks:
1. **Tuning Retrieval**:
   - **Option Hybrid**: Implement BM25 (sparse) kết hợp với Vector (dense).
   - **Option Rerank**: Dùng Jina Reranker để sắp xếp lại `top_20` kết quả đầu tiên.
2. **Evaluation Sơ bộ**:
   - Dùng hàm `compare_retrieval_strategies()` để so sánh độ chính xác của Baseline vs Variant.
3. **Logging**:
   - Ghi lại các thay đổi và kết quả thí nghiệm vào `docs/tuning-log.md`.

---

## 🔴 Sprint 4: Evaluation & Final Report
**File:** `eval.py` & `docs/`

### Tasks:
1. **Chạy Scorecard**:
   - Chạy bộ 10 câu hỏi kiểm thử trong `data/test_questions.json`.
   - Tính toán các chỉ số: `Faithfulness`, `Answer Relevance`, `Context Recall`.
2. **Hoàn thiện Documentation**:
   - Cập nhật sơ đồ kiến trúc vào `docs/architecture.md`.
   - Tổng hợp kết quả so sánh A/B.
3. **Nộp bài**:
   - Kiểm tra lại toàn bộ file code và báo cáo.
