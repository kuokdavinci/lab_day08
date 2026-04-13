# Tuning Log — RAG Pipeline (Day 08 Lab)

> Template: Ghi lại mỗi thay đổi và kết quả quan sát được.
> A/B Rule: Chỉ đổi MỘT biến mỗi lần.

---

## Baseline (Sprint 2)

**Ngày:** 13/04/2026
**Config:**
```
retrieval_mode = "dense"
chunk_size = 400 tokens
overlap = 80 tokens
top_k_search = 10
top_k_select = 3
use_rerank = False
llm_model = "gpt-4o-mini"
```

**Scorecard Baseline:**
| Metric | Average Score |
|--------|--------------|
| Faithfulness | 5 /5 |
| Answer Relevance | 2 /5 |
| Context Recall | 3 /5 |
| Completeness | 2 /5 |

**Câu hỏi yếu nhất (điểm thấp):**
- `Ai phải phê duyệt để cấp quyền Level 3?`: Điểm score thấp (0.45) dù lấy đúng file, cho thấy vector search chưa thực sự mạnh với các câu hỏi có từ khóa kỹ thuật.

**Giả thuyết nguyên nhân (Error Tree):**
- [ ] Indexing: Chunking cắt giữa điều khoản
- [ ] Indexing: Metadata thiếu effective_date
- [x] Retrieval: Dense bỏ lỡ exact keyword / alias (đặc biệt các mã lỗi như ERR-403)
- [ ] Retrieval: Top-k quá ít → thiếu evidence
- [x] Generation: Prompt không đủ grounding
- [ ] Generation: Context quá dài → lost in the middle

-----

## Variant 1 (Sprint 3)

**Ngày:** 13/04/2026  
**Biến thay đổi:**  retrieval_mode
**Lý do chọn biến này:**
> Chọn hybrid vì q07 (alias query) và q09 (mã lỗi ERR-403) đều thất bại với dense. Muốn kiểm thử khả năng tìm kiếm dựa theo keyword của mô hình.
**Config thay đổi:**
```
retrieval_mode = "hybrid" 
# Các tham số còn lại giữ nguyên như baseline
```

**Scorecard Variant 1:**
| Metric | Baseline | Variant 1 | Delta |
|--------|----------|-----------|-------|
| Faithfulness | 4.1/5 | 3.7/5 | -0.4 |
| Answer Relevance | 4.7/5 | 4.6/5 | -0.1 |
| Context Recall | 3.6/5 | 5/5 | 0.00 |
| Completeness | 3.6/5 | 3.8/5 | +0.2 |

**Nhận xét:**
Mặt bằng chung variant 1 chỉ cải thiện mức hoàn thiện của câu trả lời. Không tốt về mảng trung thực.

**Kết luận:**
> Chỉ tốt hơn về mảng trả lời thông tin đầy đủ, keyword chính xác hơn, còn lại mặt bằng chung không tốt bằng baseline

---

## Variant 2 (nếu có thời gian)

**Biến thay đổi:** use_rerank 
**Config:**
```
use_rerank = True
```

**Scorecard Variant 2:**
| Metric | Baseline | Variant 1 | Variant 2 | Best |
|--------|----------|-----------|-----------|------|
| Faithfulness | 4.2/5 | 3.7/5 |4.1 | Baseline|
| Answer Relevance | 4.7/5 | 4.6/5 |4.4  | Baseline|
| Context Recall | 3.6/5 | 5/5 | 5/5 |Variant 2|
| Completeness | 3.6/5 | 3.8/5 | 4/5 |Variant 2|

---

## Tóm tắt học được

> TODO (Sprint 4): Điền sau khi hoàn thành evaluation.

1. **Lỗi phổ biến nhất trong pipeline này là gì?**
   > Trả lời không đầy đủ. Thiếu dữ kiện 

2. **Biến nào có tác động lớn nhất tới chất lượng?**
   > Retrieve mode, nó cải thiển một cách rõ rệt Context recall, các thông số còn lại thì không khác biệt quá lớn so với baseline

3. **Nếu có thêm 1 giờ, nhóm sẽ thử gì tiếp theo?**
   > Tiếp tục tìm hiểu và tuning các thông số như trọng số giữa dense và sparse để đạt kết quả tốt hơn
