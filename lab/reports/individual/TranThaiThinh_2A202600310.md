# Báo Cáo Cá Nhân — Lab Day 08: RAG Pipeline

**Họ và tên:** Trần Thái Thịnh - 2A202600310

**Vai trò trong nhóm:** Tech Lead 

**Ngày nộp:** 13/04/2026

---

## 1. Tôi đã làm gì trong lab này? (100-150 từ)

- Nhận vai trò **Tech Lead**, trực tiếp thực hiện nhiệm vụ chính trong **Sprint 2**.
-  Thực hiện luồng RAG thông qua file `rag_answer.py`. 
-  Thực hiện truy vấn vector từ ChromaDB và hàm `call_llm` để kết nối với model LLM. Tiếp nhận data đã index từ Sprint 1, chuyển thành các kcontext block có cấu trúc và thiết lập hệ thống Grounded Prompt để đảm bảo AI trả ra câu trả lời có citation. 

---

## 2. Điều tôi hiểu rõ hơn sau lab này (100-150 từ)

- **Chunking:**  Việc cấu hình `overlap` hợp lý là khá quan trọng cho việc giữ lại ngữ cảnh ở các điểm giao giữa các đoạn, tránh làm mất thông tin quan trọng khi AI xử lý.

- Việc áp dụng **Grounded Prompting** với các quy tắc trích dẫn có citation giúp kiểm soát các lỗi Hallucination khá hiệu quả, đảm bảo tính minh bạch cho câu trả lời.
---

## 3. Điều tôi ngạc nhiên hoặc gặp khó khăn (100-150 từ) ( Em xin trình bày về trong quá trình nghe giảng )
- Được giảng viên cung cấp khá nhiều các để xử lý bài toán RAG khi gặp các vấn đề 
     + Có thể mở rộng chunk , trong trường hợp cần retrieval cần ít tốn context mà thông tin cần đầy đủ.
     + Được hướng dẫn các xư lý thông tin dạng bảng, nên thực hiện chuyển thông tin bằng -> HTML...
---

## 4. Phân tích một câu hỏi trong scorecard (150-200 từ)

**Câu hỏi:** "SLA xử lý ticket P1 là bao lâu?"

**Phân tích:** 
- **Kết quả:** Hệ thống Baseline đã trả lời hoàn toàn chính xác: "15 phút cho phản hồi ban đầu và 4 giờ để khắc phục". AI đã trích dẫn đúng nguồn tài liệu là `support/sla-p1-2026.pdf`.
- **Đánh giá luồng:** Hệ thống hoạt động tốt nhờ Indexing ở Sprint 1 đã thực hiện chunk dữ liệu theo paragraph hợp lý. Hàm `retrieve_dense` đã tìm thấy đoạn văn bản chứa thông tin SLA với similarity score rất tốt (~0.47), đủ để vượt qua ngưỡng lọc dữ liệu nhiễu.
- **Biến thể:** Tuy kết quả đúng, nhưng similarity score vẫn có thể bị loãng nếu câu hỏi chứa quá nhiều từ thừa. Nếu áp dụng thêm bước Rerank ở Sprint 3, chúng ta có thể đẩy các đoạn văn bản chứa giá trị số (15 phút, 4 giờ) lên vị trí ưu tiên cao hơn, giúp AI đưa ra câu trả lời tốt hơn.

---

## 5. Nếu có thêm thời gian, tôi sẽ làm gì? (50-100 từ)

Nếu có thêm thời gian, em sẽ làm **Hybrid Retrieval (kết hợp Dense + Sparse)**.Việc bổ sung thuật toán BM25 (keyword search) sẽ giúp bắt các từ khóa đặc thù này, giúp nâng cao đáng kể tỷ lệ Recall cho những dữ liệu mang tính kỹ thuật cao.

---

*Lưu file này với tên: `reports/individual/[ten_ban].md`*
*Ví dụ: `reports/individual/nguyen_van_a.md`*
