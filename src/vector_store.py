import json
import math
import re
from collections import Counter
from pathlib import Path

import numpy as np

from ingest import load_policy_documents
from chunking import chunk_documents


VECTOR_STORE_PATH = Path("data/vector_store.json")


def tokenize(text: str) -> list[str]:
    return re.findall(r"\b\w+\b", text.lower())


def build_vocabulary(chunks: list[dict]) -> list[str]:
    vocab = set()

    for chunk in chunks:
        vocab.update(tokenize(chunk["text"]))

    return sorted(vocab)


def compute_idf(chunks: list[dict], vocabulary: list[str]) -> dict:
    num_docs = len(chunks)
    idf = {}

    for term in vocabulary:
        doc_count = sum(1 for chunk in chunks if term in set(tokenize(chunk["text"])))
        idf[term] = math.log((1 + num_docs) / (1 + doc_count)) + 1

    return idf


def embed_text(text: str, vocabulary: list[str], idf: dict) -> list[float]:
    tokens = tokenize(text)
    counts = Counter(tokens)
    total_tokens = len(tokens) or 1

    vector = []

    for term in vocabulary:
        tf = counts[term] / total_tokens
        vector.append(tf * idf[term])

    return vector


def build_vector_store():
    docs = load_policy_documents()
    chunks = chunk_documents(docs)

    vocabulary = build_vocabulary(chunks)
    idf = compute_idf(chunks, vocabulary)

    stored_chunks = []

    for chunk in chunks:
        vector = embed_text(chunk["text"], vocabulary, idf)

        stored_chunks.append({
            "source": chunk["source"],
            "title": chunk["title"],
            "text": chunk["text"],
            "embedding": vector,
        })

    vector_store = {
        "vocabulary": vocabulary,
        "idf": idf,
        "chunks": stored_chunks,
    }

    VECTOR_STORE_PATH.write_text(json.dumps(vector_store, indent=2), encoding="utf-8")

    print(f"Stored {len(stored_chunks)} embedded chunks.")
    print(f"Vocabulary size: {len(vocabulary)}")
    print(f"Vector store saved to {VECTOR_STORE_PATH}")


def load_vector_store():
    return json.loads(VECTOR_STORE_PATH.read_text(encoding="utf-8"))


def cosine_similarity(a: list[float], b: list[float]) -> float:
    a_array = np.array(a)
    b_array = np.array(b)

    denominator = np.linalg.norm(a_array) * np.linalg.norm(b_array)

    if denominator == 0:
        return 0.0

    return float(np.dot(a_array, b_array) / denominator)


def retrieve_vector_chunks(question: str, top_k: int = 3) -> list[dict]:
    vector_store = load_vector_store()

    vocabulary = vector_store["vocabulary"]
    idf = vector_store["idf"]
    chunks = vector_store["chunks"]

    question_embedding = embed_text(question, vocabulary, idf)

    scored_chunks = []

    for chunk in chunks:
        score = cosine_similarity(question_embedding, chunk["embedding"])

        scored_chunks.append({
            "source": chunk["source"],
            "title": chunk["title"],
            "text": chunk["text"],
            "score": score,
        })

    scored_chunks.sort(key=lambda x: x["score"], reverse=True)

    return scored_chunks[:top_k]


if __name__ == "__main__":
    build_vector_store()

    question = "How many PTO days do employees receive?"
    results = retrieve_vector_chunks(question)

    print(f"\nQuestion: {question}")

    for result in results:
        print("\n---")
        print(f"Source: {result['source']}")
        print(f"Score: {result['score']:.4f}")
        print(result["text"])