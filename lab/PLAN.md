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

## 🔴 Sprint 4: Evaluation, Documentation & Final Report ✓ COMPLETED
**File:** `eval.py` & `docs/` & `reports/`

### Tasks:
1. **Chấm điểm (Evaluation)** ✓:
   - [x] Sử dụng bộ 10 câu hỏi trong `data/test_questions.json`.
   - [x] Thực hiện chấm điểm qua `eval.py` để tính các chỉ số: `Faithfulness`, `Answer Relevance`, `Context Recall`, `Completeness`.
   - [x] **BONUS**: Implement LLM-as-Judge để tự động hóa việc chấm điểm (✓ GPT-4o-mini)

2. **So sánh A/B (A/B Testing)** ✓:
   - [x] Chạy `run_scorecard(BASELINE_CONFIG)` → scorecard_baseline.md
   - [x] Chạy `run_scorecard(VARIANT_CONFIG)` → scorecard_variant.md (Champion: Hybrid + Reranker)
   - [x] Sử dụng `compare_ab()` để phân tích delta → ab_comparison.csv

3. **Hoàn thiện Tài liệu (Documentation)** ✓:
   - [x] `docs/architecture.md`: Cập nhật Sprint 3 Champion config + Sprint 4 Evaluation Framework
   - [x] `docs/tuning-log.md`: Ghi lại kết quả thí nghiệm, nhận xét chi tiết, lessons learned

4. **Báo cáo cá nhân (Individual Reports)**:
   - [ ] Viết bài phân tích (500-800 từ) về phần việc mình đảm nhận và rút kinh nghiệm thực tế (Reports Owner)

### Definition of Done (DOD):
- [x] Demo chạy trơn tru: `python index.py && python rag_answer.py && python eval.py`. ✓
- [ ] Báo cáo nhóm và báo cáo cá nhân đầy đủ trong thư mục `reports/`.
- [ ] Log chạy grading (`logs/grading_run.json`) sẵn sàng trước 18:00.

### Results:
**Champion: Variant (Hybrid + Reranker)**
- **Faithfulness**: 4.20 → **4.30** (+0.10 ✓)
- **Completeness**: 3.90 → **4.10** (+0.20 ✓)
- **Context Recall**: 5.00 (Perfect both)

**Key Findings:**
- q04 (Refund digital goods): Hybrid + Reranker xử lý được ngoại lệ kỹ thuật số
- q06 (SLA Escalation): Reranker chọn đúng chunks về escalation workflow
- No tradeoff: Faithfulness, Relevance giữ ổn định
