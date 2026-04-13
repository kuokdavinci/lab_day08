# Báo Cáo Cá Nhân — Lab Day 08: RAG Pipeline

**Họ và tên:** Nguyễn Văn Thạch - 2A202600237
**Vai trò trong nhóm:** Evaluation Specialist (Sprint 4 Owner)
**Ngày nộp:** 13/04/2026
**Độ dài yêu cầu:** 500–800 từ

---

## 1. Tôi đã làm gì trong lab này? (100-150 từ)

Trong lab này, tôi làm phần **Sprint 4: Evaluation & Scorecard**. Công việc của tôi tập trung vào việc hiện thực hóa khung đánh giá tự động cho hệ thống RAG. Cụ thể, tôi đã lập trình các hàm `LLM-as-Judge` trong file `eval.py` để chấm điểm 4 chỉ số quan trọng: Faithfulness (độ trung thực), Answer Relevance (độ liên quan), Context Recall (khả năng truy xuất) và Completeness (độ đầy đủ).

Tôi đã thiết lập quy trình chạy Benchmark tự động để so sánh Baseline (Dense Retrieval) và Variant (Hybrid + Rerank). Trong quá trình này, tôi cũng đã xử lý các lỗi logic về tính toán Delta trong báo cáo và tối ưu hóa script để xử lý lỗi kết nối API. Công việc của tôi đóng vai trò là "mắt xích cuối cùng", giúp Tech Lead và các thành viên khác định lượng được hiệu quả của các thay đổi kỹ thuật ở Sprint 1, 2 và 3, từ đó có cơ sở để hoàn thiện tài liệu `tuning-log.md`.

---

## 2. Điều tôi hiểu rõ hơn sau lab này (100-150 từ)

Sau lab này, tôi đã thực sự hiểu sâu về khái niệm **Evaluation Loop** và tầm quan trọng của việc "định lượng hóa" chất lượng AI. Trước đây, tôi thường đánh giá chatbot bằng cách hỏi thử một vài câu cảm tính. Qua lab, tôi nhận ra rằng RAG rất dễ gặp lỗi "nhiễu ngữ cảnh" (context noise).

Tôi hiểu rõ sự khác biệt giữa **Faithfulness** và **Answer Relevance**: Một câu trả lời có thể nghe rất hay và liên quan (High Relevance) nhưng lại hoàn toàn là bịa đặt do không có trong bằng chứng (Low Faithfulness). Tôi cũng học được cách sử dụng LLM để chấm điểm cho chính LLM khác, đây là một kỹ thuật mạnh mẽ giúp scale quy trình kiểm thử mà không cần sức người đọc hàng nghìn câu trả lời. Ngoài ra, việc hiểu về **Context Recall** giúp tôi nhận ra rằng nếu bước Retrieval fail, thì dù LLM có thông minh đến đâu cũng không thể cứu vãn được câu trả lời.

---

## 3. Điều tôi ngạc nhiên hoặc gặp khó khăn (100-150 từ)

Điều làm tôi ngạc nhiên nhất là việc tăng thêm tính năng (Variant) không phải lúc nào cũng mang lại kết quả tốt hơn. Khi chúng tôi thêm Hybrid Search và Rerank, giả thuyết ban đầu là kết quả sẽ vượt trội Baseline. Tuy nhiên, thực tế Eval cho thấy một số câu hỏi (như Q09) bị giảm điểm do Hybrid mang về quá nhiều "nhiễu" keyword, khiến LLM bị bối rối.

Khó khăn lớn nhất tôi gặp phải là lỗi logic "Deceptively Simple" trong code tính toán kết quả: giá trị Delta hiển thị `N/A` khi độ lệch bằng `0`. Tôi đã mất một khoảng thời gian để nhận ra lỗi nằm ở cách Python xử lý truthiness (`if delta:`), qua đó học được bài học quan trọng về việc sử dụng `is not None` khi làm việc với các chỉ số đo lường. Ngoài ra, sự thiếu ổn định của kết nối API khi chạy đánh giá hàng loạt cũng là một thử thách, buộc tôi phải thêm các cơ chế catch lỗi để pipeline không bị dừng đột ngột.

---

## 4. Phân tích một câu hỏi trong scorecard (150-200 từ)

**Câu hỏi:** [q06] "Escalation trong sự cố P1 diễn ra như thế nào?"

**Phân tích:**
Đây là một câu hỏi rất thú vị vì nó thể hiện rõ sự khác biệt giữa hai chiến lược tìm kiếm.

- **Baseline (Dense):** Trả lời đúng một phần nhưng rất chung chung, thiếu các mốc thời gian cụ thể (10 phút chuyển Senior, 30 phút chuyển Manager). Điểm Completeness chỉ đạt 2/5. Nguyên nhân là do Dense Embedding tập trung vào ngữ cảnh "SLA" chung và mang về các đoạn mô tả thời hạn phản hồi, nhưng lại bỏ lỡ đoạn bảng biểu (table) quy định về Matrix Escalation nằm ở cuối file.
- **Variant (Hybrid + Rerank):** Cải thiện vượt bậc với điểm 5/5 ở hầu hết các metric. Nhờ Hybrid Search, từ khóa "Escalation" (vốn là một keyword hiếm và đặc thù) đã giúp BM25 lấy đúng chính xác file `support/sla-p1-2026.pdf`. Quan trọng hơn, Jina Reranker đã nhận diện được chunk chứa quy trình Escalation có độ liên quan cao nhất và đẩy nó lên vị trí [1].
- **Kết luận:** Trong trường hợp này, sự kết hợp giữa tìm kiếm từ khóa chính xác và chấm điểm lại bằng Rerank đã giải quyết triệt để lỗi "lạc đề" của mô hình Embedding đơn thuần, giúp LLM có đầy đủ chứng cứ để trả lời chi tiết và chính xác.

---

## 5. Nếu có thêm thời gian, tôi sẽ làm gì? (50-100 từ)

Tôi sẽ tập trung vào việc **tinh chỉnh trọng số Hybrid Search (Hybrid Weight Tuning)**. Kết quả Eval hiện tại cho thấy việc dùng RRF mặc định đang mang lại quá nhiều nhiễu cho các câu hỏi đơn giản. Tôi muốn thử nghiệm các tỷ lệ khác nhau (ví dụ: 0.7 cho Dense và 0.3 cho Sparse) để tận dụng khả năng hiểu ngữ cảnh của Embedding mà vẫn giữ được độ chính xác tuyệt đối của BM25 cho các mã lỗi như ERR-403. Ngoài ra, tôi muốn implement thêm cơ chế `Context Filtering` dựa trên ngưỡng điểm (threshold) của Reranker để loại bỏ các chunk rác trước khi đưa vào LLM.

---
