# Báo Cáo Cá Nhân — Lab Day 08: RAG Pipeline

**Họ và tên:**  Lê Trung Anh Quốc
**Vai trò trong nhóm:** Tech Lead (Sprint 1) / Eval Hepler / Documentation Owner  
**Ngày nộp:** 13/4/2026  
**Độ dài yêu cầu:** 500–800 từ

---

Trong lab này, tôi đảm nhận vai trò Tech Lead và Documentation Owner, tập trung vào việc tối ưu hóa và đánh giá hệ thống RAG. Cụ thể, tôi đã:
- Triển khai phương pháp **Header-based Chunking** kết hợp với tách đoạn (Paragraph splitting) để đảm bảo tính toàn vẹn về mặt ngữ nghĩa cho các tài liệu kỹ thuật và chính sách.
- Thiết lập hệ thống đánh giá A/B testing để so sánh giữa Baseline (Dense Retrieval) và các Variant (Hybrid Search + Reranker).
- Thực hiện **Finetune các thông số kỹ thuật**: Tăng `top_k_search` từ 10 lên 15 và `top_k_select` từ 3 lên 5 để cung cấp thêm ngữ cảnh cho mô hình.
- Cấu hình **Hybrid Search (Vector + BM25)** và tích hợp **Cross-Encoder Reranker** để cải thiện độ chính xác trong việc truy xuất các từ khóa đặc thù như mã lỗi (ERR-403) hay các cấp độ phê duyệt (Level 3).
- Hiệu chỉnh System Prompt để tăng cường khả năng **Grounding**, giúp mô hình biết cách từ chối trả lời (abstain) khi không tìm thấy thông tin trong ngữ cảnh (như trường hợp câu q09).


---

## 2. Điều tôi hiểu rõ hơn sau lab này (100-150 từ)

Sau lab này, tôi đã hiểu sâu sắc về sự đánh đổi (**Trade-offs**) giữa các tiêu chí đánh giá trong hệ thống RAG:
- **Completeness vs Relevance**: Khi tăng lượng context được đưa vào (top_k_select), điểm Completeness tăng (từ 3.9 lên 4.1) nhưng điểm Relevance lại giảm (-0.40) do LLM bị nhiễu bởi quá nhiều thông tin không liên quan (hiện tượng "Lost in the Middle").
- **Tầm quan trọng của Hybrid Search**: Vector search mạnh về ngữ nghĩa nhưng thường bỏ lỡ các từ khóa chính xác (Exact keywords). Việc kết hợp BM25 là bắt buộc đối với các hệ thống tra cứu tài liệu kỹ thuật có nhiều mã hiệu hoặc thuật ngữ chuyên biệt.
- **Vai trò của Reranker**: Reranker hoạt động như một bộ lọc chất lượng cao, giúp sắp xếp lại các kết quả từ Hybrid Search một cách thông minh hơn, đặc biệt hiệu quả cho các câu hỏi phức tạp cần kết hợp thông tin từ nhiều đoạn (multi-hop).


---

## 3. Điều tôi ngạc nhiên hoặc gặp khó khăn (100-150 từ)

- **Khó khăn nhất**: Việc debug câu hỏi về "Access Control" (q03) khiến tôi tốn nhiều thời gian. Dù đã dùng Hybrid + Reranker, điểm Faithfulness vẫn thấp (2/5). Sau khi kiểm tra log, tôi phát hiện do chunking cắt ngang bảng phân quyền, khiến LLM hiểu sai mối quan hệ giữa các cấp độ phê duyệt.
- **Điều gây ngạc nhiên**: Tôi ban đầu giả định rằng càng cung cấp nhiều context thì câu trả lời càng tốt. Tuy nhiên, kết quả Variant 2 cho thấy điểm Relevance giảm mạnh (từ 4.7 xuống 4.3). Điều này minh chứng cho việc LLM có thể bị "confused" khi phải xử lý context quá dài và chứa nhiều nội dung gây nhiễu, đặc biệt là với các câu hỏi không có câu trả lời trong docs (q09).
- **Lỗi debug**: Việc cấu hình tham số reranker đòi hỏi tinh chỉnh nhiều lần để cân bằng giữa độ trễ (latency) và chất lượng phản hồi.


---

## 4. Phân tích một câu hỏi trong scorecard (150-200 từ)

**Câu hỏi:** q06 — "Escalation trong sự cố P1 diễn ra như thế nào?"

**Phân tích:**
- **Baseline (Dense Search)**: Trả lời đúng về thời gian phản hồi (15 phút) nhưng chỉ đạt điểm **2/5 về Completeness**. Lý do là Baseline chỉ lấy được đoạn thông tin đầu tiên về SLA mà bỏ lỡ đoạn mô tả quy trình leo thang (escalation) nằm ở phần sau của tài liệu do cơ chế cắt chunk cố định (Fixed-size chunking) làm phân mảnh ngữ cảnh.
- **Lỗi nằm ở**: **Retrieval**. Vector search đơn thuần không ưu tiên đủ các đoạn chứa từ khóa "escalation" khi câu hỏi tập trung vào quy trình phức tạp.
- **Variant 2 (Hybrid + Reranker)**: Đạt điểm tối đa **5/5 về Completeness**. Sự cải thiện này đến từ hai yếu tố:
    1. **Hybrid Search**: BM25 giúp bắt đúng từ khóa "Escalation" và "P1".
    2. **Reranker**: Với `top_k_search=15`, Reranker có đủ ứng viên để chọn ra chính xác các chunk chứa toàn bộ workflow leo thang lên Senior Engineer (sau 10 phút).
    3. **Header-based Chunking**: Giúp gom các quy định liên quan đến cùng một mục tiêu (SLA/Escalation) vào các đoạn có ý nghĩa trọn vẹn hơn.


---

## 5. Nếu có thêm thời gian, tôi sẽ làm gì? (50-100 từ)

Tôi sẽ tập trung vào hai hướng cải tiến cụ thể:
1. **Query Transformation (HyDE)**: Thử nghiệm kỹ thuật tạo văn bản giả định để cải thiện retrieval cho các câu hỏi về mã lỗi kỹ thuật (như q09), giúp vector search tìm kiếm hiệu quả hơn dựa trên mô tả thay vì chỉ keyword.
2. **Metadata Filtering**: Triển khai lọc theo `effective_date` để giải quyết triệt để vấn đề "Policy Versioning" trong câu q10, đảm bảo mô hình luôn ưu tiên thông tin mới nhất thay vì bị lẫn lộn giữa các phiên bản tài liệu cũ và mới.
3. **Optimize Top-K**: Giảm `top_k_select` xuống 4 để cố gắng phục hồi điểm Relevance mà không làm mất đi lợi ích về Completeness.
4. **Query Rewriting**: Sử dụng LLM để viết lại câu hỏi, thêm các từ khóa liên quan, giúp vector search tìm kiếm hiệu quả hơn.

---

*Lưu file này với tên: `reports/individual/[ten_ban].md`*
*Ví dụ: `reports/individual/nguyen_van_a.md`*
