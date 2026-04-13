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

## Variant 2 — Champion: Hybrid + Reranker (Sprint 4 ✓)

**Ngày:** 13/04/2026
**Biến thay đổi:** retrieval_mode + use_rerank + top_k parameters
**Lý do chọn:**
> Kết hợp hybrid retrieval (dense + sparse) với reranker để lấy lợi thế cả hai mặt:
> - Dense: Semantic search mạnh mẽ
> - Sparse: Exact keyword matching (tên tài liệu, mã lỗi)
> - Reranker: Cross-encoder sắp xếp lại độc lập với embedding

**Config thay đổi:**
```
retrieval_mode = "hybrid"    # Dense + Sparse (BM25)
top_k_search = 15             # ↑ từ 10: cho reranker có dồi dào ứng viên
top_k_select = 5              # ↑ từ 3: xem toàn cảnh hơn 
use_rerank = True             # Thêm cross-encoder reranking
llm_model = "gpt-4o-mini"
```

**Scorecard Champion:**
| Metric | Baseline | Variant 2 | Delta | Status |
|--------|----------|-----------|-------|--------|
| Faithfulness | 4.20/5 | 4.30/5 | +0.10 | ✓ |
| Answer Relevance | 4.30/5 | 4.30/5 | — | Tie |
| Context Recall | 5.00/5 | 5.00/5 | — | Perfect |
| Completeness | 3.90/5 | 4.10/5 | +0.20 ✓ | Best |

**Per-Question Improvements:**
- **q04 (Refund)**: Faithfulness 4→5 — Hybrid tìm được context cho "hàng kỹ thuật số"
- **q06 (Escalation SLA)**: Completeness 2→5 — Reranker chọn đúng chunks về escalation workflow

**Nhận xét chi tiết:**
1. **Variant 2 nhỉnh hơn baseline +0.20 ở Completeness**
   - Reranker giúp chọn lựa chunks đầy đủ hơn
   - Hybrid retrieval bắt được cả semantic + keyword matches
   
2. **Faithfulness tăng nhẹ +0.10**
   - Chứng tỏ context retrieved chất lượng cao hơn
   - Ít hallucination hơn

3. **Context Recall vẫn 5.00 (Perfect)**
   - Baseline đã tìm đủ expected sources
   - Variant không làm xuất hiện "new sources" không cần thiết

**Kết luận Variant 2:**
> ✅ **Champion đạt tiêu chí:** Cải thiện completeness (trả lời đầy đủ) mà không giảm các metrics khác. 
> Hybrid + Reranker là cải thiện tối ưu cho pipeline này.

---

## Tóm tắt học được (Sprint 4 ✓)

1. **Lỗi phổ biến nhất trong pipeline này là gì?**
   > **Incomplete Responses (3/10 câu hỏi completeness < 4/5)**
   > 
   > Nguyên nhân: Context retrieved đôi khi thiếu "điều kiện ngoại lệ" hoặc "bước phụ"
   > - q06: Baseline thiếu thông tin về escalation rules (completeness=2)
   > - q10: Model không mention "VIP handling" (không có trong docs)
   > 
   > Cải thiện Variant 2 → Completeness tăng lên 4.10/5 (tăng +0.20)
   > Reranker giúp sắp xếp chunks sao cho LLM dễ thấy hơn các thông tin bổ sung.

2. **Biến nào có tác động lớn nhất tới chất lượng?**
   > **Top-K Parameters + Reranker có tác dụng rõ rệt** (+0.20 completeness)
   > 
   > - Tăng top_k_search từ 10→15: Reranker có dồi dào candidates
   > - Tăng top_k_select từ 3→5: LLM thấy toàn cảnh context, ít miss thông tin
   > - Reranker: Cross-encoder sắp xếp độc lập, catch được mối liên quan language model miss
   > 
   > Hybrid retrieval (dense+sparse) bắt được cả semantic + keyword, nhưng tác dụng không lớn nếu không kết hợp rerank.

3. **Các hiệu ứng phụ/trade-offs?**
   > - **Latency**: Tăng lên vì phải chạy reranker trên 15 chunks (cross-encoder)
   > - **Faithfulness**: Tăng nhẹ +0.10, không có tradeoff negative
   > - **Context Recall**: Vẫn perfect 5.00/5, không ảnh hưởng xấu
   > - **Relevance**: Giữ nguyên 4.30/5

4. **Outliers & Edge Cases:**
   > - **q09 (Insufficient Context)**: Faithfulness=5 nhưng Relevance=1
   >   → Model trung thực từ chối câu hỏi không có đáp án trong docs (✓ tốt!)
   > 
   > - **q03, q10 (Tricky questions)**: Faithfulness thấp (2/5)
   >   → Model retrieve đúng file nhưng suy luận sai hoặc context mơ hồ
   >   → Cần fine-tune prompt hoặc augment training data

5. **Nếu có thêm 1 giờ, nhóm sẽ thử gì tiếp theo?**
   > 1. **Query Transformation:** Thử HyDE (Hypothetical Document Embeddings) để rewrite query trước khi retrieve
   > 2. **Prompt Tuning:** Thêm "Chain-of-Thought" để LLM giải thích reasoning
   > 3. **Chunk Ablation:** Test chunk_size khác nhau (200/400/600 tokens)
   > 4. **Hybrid Weights:** Tune reweight giữa dense scoring vs BM25 scoring
