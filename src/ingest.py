from pathlib import Path


def load_policy_documents(policy_dir: str = "data/policies") -> list[dict]:
    """
    Load all markdown policy documents from the policy directory.

    Each document is stored as a dictionary with:
    - source: the filename
    - title: the first heading in the file
    - text: the full document text
    """
    documents = []
    policy_path = Path(policy_dir)

    for file_path in sorted(policy_path.glob("*.md")):
        text = file_path.read_text(encoding="utf-8")

        title = file_path.stem
        for line in text.splitlines():
            if line.startswith("# "):
                title = line.replace("# ", "").strip()
                break

        documents.append({
            "source": file_path.name,
            "title": title,
            "text": text
        })

    return documents


if __name__ == "__main__":
    docs = load_policy_documents()
    print(f"Loaded {len(docs)} policy documents.")

    for doc in docs:
        print(f"- {doc['title']} ({doc['source']})")