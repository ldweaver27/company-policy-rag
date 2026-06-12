import os
from dotenv import load_dotenv
from groq import Groq

from ingest import load_policy_documents
from chunking import chunk_documents
from retrieval import retrieve_relevant_chunks


load_dotenv()


def build_context(chunks: list[dict]) -> str:
    context_parts = []

    for i, chunk in enumerate(chunks, start=1):
        context_parts.append(
            f"[Source {i}: {chunk['title']} - {chunk['source']}]\n"
            f"{chunk['text']}"
        )

    return "\n\n".join(context_parts)


def generate_answer(question: str, context: str) -> str:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""
You are a company policy assistant for BrightWave Technologies.

Answer the user's question using only the provided policy context.

Rules:
- If the answer is not in the context, say: "I can only answer based on the provided company policy documents."
- Keep the answer concise.
- Always cite the source number(s) used.

Policy Context:
{context}

User Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=300,
    )

    return response.choices[0].message.content


def answer_question(question: str) -> dict:
    docs = load_policy_documents()
    chunks = chunk_documents(docs)
    retrieved_chunks = retrieve_relevant_chunks(question, chunks, top_k=3)
    context = build_context(retrieved_chunks)
    answer = generate_answer(question, context)

    return {
        "question": question,
        "answer": answer,
        "context": context,
        "sources": retrieved_chunks,
    }


if __name__ == "__main__":
    question = "How many PTO days do employees receive?"
    result = answer_question(question)

    print("Question:")
    print(result["question"])

    print("\nAnswer:")
    print(result["answer"])

    print("\nRetrieved Context:")
    print(result["context"])