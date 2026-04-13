import sys
import io
from pathlib import Path
# Ép kiểu UTF-8 cho console
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.append(str(Path(__file__).parent))
from rag_answer import rag_answer

query = "SLA xử lý ticket P1 đã thay đổi như thế nào với phiên bản trước?"

print(f"\nQUERY: {query}")
print("="*60)

result = rag_answer(
    query=query,
    retrieval_mode="hybrid",
    use_rerank=True,
    verbose=True
)

print("\n" + "="*60)
print(f"FINAL ANSWER: {result['answer']}")
