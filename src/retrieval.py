import re
from ingest import load_policy_documents
from chunking import chunk_documents


def tokenize(text: str) -> set[str]:
    """
    Convert text into a set of lowercase words.
    """
    return set(re.findall(r"\b\w+\b", text.lower()))


def retrieve_relevant_chunks(question: str, chunks: list[dict], top_k: int = 3) -> list[dict]:
    """
    Retrieve the top_k chunks with the most word overlap with the question.
    """
    question_words = tokenize(question)
    scored_chunks = []

    for chunk in chunks:
        chunk_words = tokenize(chunk["text"] + " " + chunk["title"] + " " + chunk["source"])
        score = len(question_words.intersection(chunk_words))

        if score > 0:
            scored_chunks.append({
                **chunk,
                "score": score
            })

    scored_chunks.sort(key=lambda x: x["score"], reverse=True)
    return scored_chunks[:top_k]


if __name__ == "__main__":
    docs = load_policy_documents()
    chunks = chunk_documents(docs)

    question = "How many PTO days do employees receive?"
    results = retrieve_relevant_chunks(question, chunks)

    print(f"Question: {question}")
    print(f"Retrieved {len(results)} chunks:")

    for result in results:
        print("\n---")
        print(f"Source: {result['source']}")
        print(f"Score: {result['score']}")
        print(result["text"])