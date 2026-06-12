import json
import time
import numpy as np

from rag import answer_question


def load_questions():
    with open("data/evaluation_questions.json", "r") as f:
        return json.load(f)


def evaluate():
    questions = load_questions()

    results = []
    latencies = []

    print(f"Running {len(questions)} evaluation questions...\n")

    for item in questions:
        question = item["question"]

        start_time = time.time()
        result = answer_question(question)
        latency = time.time() - start_time

        latencies.append(latency)

        results.append({
            "question": question,
            "answer": result["answer"],
            "expected_answer": item["expected_answer"],
            "expected_source": item["expected_source"],
            "latency": latency,
        })

        print(f"✓ {question}")
        print(f"  Latency: {latency:.2f}s")

    avg_latency = float(np.mean(latencies))
    p50_latency = float(np.percentile(latencies, 50))
    p95_latency = float(np.percentile(latencies, 95))

    print("\n========== SUMMARY ==========")
    print(f"Questions Evaluated: {len(results)}")
    print(f"Average Latency: {avg_latency:.2f} seconds")
    print(f"p50 Latency: {p50_latency:.2f} seconds")
    print(f"p95 Latency: {p95_latency:.2f} seconds")

    return results


if __name__ == "__main__":
    evaluate()