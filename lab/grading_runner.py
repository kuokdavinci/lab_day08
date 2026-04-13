#!/usr/bin/env python3
"""
grading_runner.py — Chạy grading_questions.json qua pipeline SAG
Tạo logs/grading_run.json với format bắt buộc
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# UTF-8 encoding cho console
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from rag_answer import rag_answer

# =============================================================================
# CONFIG
# =============================================================================

GRADING_QUESTIONS_PATH = Path(__file__).parent / "data" / "grading_questions.json"
LOGS_DIR = Path(__file__).parent / "logs"
GRADING_RUN_OUTPUT = LOGS_DIR / "grading_run.json"

# Dùng best config (Variant Champion: Hybrid + Reranker) + tuning
GRADING_CONFIG = {
    "retrieval_mode": "hybrid",
    "top_k_search": 20,   # Tăng 15→20 để hybrid lấy chunks từ cả 2+ docs
    "top_k_select": 8,    # Tăng 5→8 để LLM thấy đầy đủ thông tin
    "use_rerank": True,
}

# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("GRADING RUNNER — Chạy 10 grading questions")
    print("=" * 70)
    
    # Load grading questions
    print(f"\nLoading grading questions từ: {GRADING_QUESTIONS_PATH}")
    try:
        with open(GRADING_QUESTIONS_PATH, "r", encoding="utf-8") as f:
            questions = json.load(f)
        print(f"✓ Tìm thấy {len(questions)} câu hỏi")
    except FileNotFoundError:
        print(f"✗ Không tìm thấy {GRADING_QUESTIONS_PATH}")
        sys.exit(1)
    
    # Ensure logs directory exists
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Run grading
    print(f"\n--- Chạy pipeline với config: {GRADING_CONFIG} ---\n")
    
    grading_log = []
    start_time = datetime.now()
    
    for i, q in enumerate(questions, 1):
        qid = q["id"]
        question = q["question"]
        points = q.get("points", 0)
        category = q.get("category", "Unknown")
        
        print(f"[{i}/{len(questions)}] {qid} ({points} điểm, {category})", end=" ... ", flush=True)
        
        try:
            # Call RAG pipeline
            result = rag_answer(
                query=question,
                retrieval_mode=GRADING_CONFIG["retrieval_mode"],
                top_k_search=GRADING_CONFIG["top_k_search"],
                top_k_select=GRADING_CONFIG["top_k_select"],
                use_rerank=GRADING_CONFIG["use_rerank"],
                verbose=False,
            )
            
            answer = result["answer"]
            sources = result.get("sources", [])
            chunks_used = result.get("chunks_used", [])
            
            # Log entry
            log_entry = {
                "id": qid,
                "question": question,
                "answer": answer,
                "sources": sources,
                "chunks_retrieved": len(chunks_used),
                "retrieval_mode": GRADING_CONFIG["retrieval_mode"],
                "use_rerank": GRADING_CONFIG["use_rerank"],
                "category": category,
                "points": points,
                "timestamp": datetime.now().isoformat(),
            }
            grading_log.append(log_entry)
            
            print(f"✓ ({len(sources)} sources)")
            
        except Exception as e:
            print(f"✗ ERROR")
            log_entry = {
                "id": qid,
                "question": question,
                "answer": f"PIPELINE_ERROR: {str(e)[:100]}",
                "sources": [],
                "chunks_retrieved": 0,
                "retrieval_mode": GRADING_CONFIG["retrieval_mode"],
                "use_rerank": GRADING_CONFIG["use_rerank"],
                "category": category,
                "points": points,
                "timestamp": datetime.now().isoformat(),
                "error": str(e)[:200],
            }
            grading_log.append(log_entry)
    
    end_time = datetime.now()
    
    # Save log
    print(f"\n--- Lưu log ---\n")
    with open(GRADING_RUN_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(grading_log, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"✓ Saved grading_run.json ({len(grading_log)} entries)")
    print(f"  Path: {GRADING_RUN_OUTPUT}")
    print(f"  Time: {end_time - start_time}")
    
    # Summary
    print(f"\n--- Summary ---")
    successful = sum(1 for entry in grading_log if "error" not in entry)
    failed = len(grading_log) - successful
    total_points = sum(entry.get("points", 0) for entry in grading_log)
    
    print(f"Successful: {successful}/{len(grading_log)}")
    print(f"Failed: {failed}/{len(grading_log)}")
    print(f"Total raw points: {total_points}")
    print(f"Grading points (if all perfect): {total_points / 98 * 30:.1f}/30")
    
    print("\n" + "=" * 70)
    print("✓ Grading completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
