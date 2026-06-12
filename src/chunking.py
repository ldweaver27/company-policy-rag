from ingest import load_policy_documents


def chunk_documents(documents):
    """
    Split documents into chunks based on markdown headings.
    """

    chunks = []

    for doc in documents:
        sections = doc["text"].split("## ")

        for section in sections:
            section = section.strip()

            if not section:
                continue

            chunks.append(
                {
                    "source": doc["source"],
                    "title": doc["title"],
                    "text": section
                }
            )

    return chunks


if __name__ == "__main__":
    docs = load_policy_documents()
    chunks = chunk_documents(docs)

    print(f"Created {len(chunks)} chunks.")

    for chunk in chunks[:5]:
        print("\n---")
        print(chunk["source"])
        print(chunk["text"][:150])