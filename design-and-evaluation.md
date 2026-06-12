# Design and Evaluation

## Project Overview

This project implements a Retrieval-Augmented Generation (RAG) application that answers questions about company policies and procedures for a fictional organization called BrightWave Technologies.

The system uses a collection of policy documents as its knowledge base and retrieves relevant information before generating responses with a Large Language Model (LLM). Answers include citations to the source policy documents used to generate the response.

---

## Architecture

The application follows a Retrieval-Augmented Generation (RAG) architecture:

1. User submits a question through the web interface or API.
2. Policy documents are loaded from the policy corpus.
3. Documents are divided into smaller searchable chunks.
4. The retrieval component identifies the most relevant chunks.
5. Retrieved chunks are formatted into a context block.
6. The context and user question are sent to the LLM.
7. The LLM generates an answer using only the retrieved context.
8. The answer and citations are returned to the user.

### Components

#### Document Corpus

The corpus consists of 10 synthetic company policy documents covering:

* PTO
* Remote Work
* Expense Reimbursement
* Holidays
* Parental Leave
* Information Security
* Business Travel
* Equipment
* Code of Conduct
* Performance Reviews

#### Ingestion

Policy documents are loaded from Markdown files located in the `data/policies` directory.

#### Chunking Strategy

Documents are split using Markdown section headings (`##`).

This produced approximately 46 searchable chunks across the corpus.

Chunking improves retrieval quality by allowing the system to search smaller sections rather than entire documents.

#### Retrieval Strategy

The system generates TF-IDF vector embeddings for document chunks and stores them in a local JSON-based vector store. User questions are embedded using the same vocabulary and retrieved using cosine similarity search. The top 3 most similar chunks are passed to the LLM.


#### Generation

The system uses the Groq API with the Llama 3.1 8B Instant model.

Retrieved chunks are inserted into the prompt as context.

The model is instructed to:

* Answer only using provided policy information
* Refuse questions outside the policy corpus
* Keep responses concise
* Include citations

#### Web Application

The application is implemented using Flask.

Endpoints include:

* `/` : Web chat interface
* `/chat` : JSON API endpoint
* `/health` : Health check endpoint

---

## Evaluation

### Evaluation Dataset

An evaluation set of 18 policy-related questions was created.

Questions cover:

* PTO
* Sick Leave
* Remote Work
* Expenses
* Holidays
* Parental Leave
* Security Policies
* Travel Policies
* Equipment Policies
* Performance Reviews

### Information Quality

Manual testing demonstrated that answers were consistently grounded in retrieved policy content.

Responses included citations referencing the supporting policy documents.

For the evaluation questions tested, answers matched the information contained in the source documents.

### System Metrics

Latency was measured across all evaluation questions.

Results:

*Results:

- Number of evaluation questions: 18
- Average latency: 0.66 seconds per query
- p50 latency: 0.33 seconds
- p95 latency: 2.35 seconds

Manual review of the 18-question evaluation set found:
- Groundedness: 18/18 answers were supported by retrieved policy evidence, or 100%.
- Citation Accuracy: 18/18 answers cited a policy document containing the supporting information, or 100%.
- Average Latency: 0.97 seconds.

### Observations

The retrieval approach performed well because the policy corpus contains highly structured documents and domain-specific terminology.

Future improvements could include:

* Embedding-based retrieval
* Vector database indexing
* Retrieval re-ranking
* Automated citation accuracy scoring

---

## Design Rationale

Fixed seeds were not required because the chunking process is deterministic and the evaluation set is fixed rather than randomly sampled.

### Why Markdown Documents?

Markdown is simple, human-readable, and easy to version control.

### Why Heading-Based Chunking?

Policy documents naturally contain sections and subsections. Splitting on headings preserves semantic meaning.


### Why Keyword Retrieval?

Keyword retrieval is lightweight, easy to explain, and performs well on a small policy corpus.

### Why Groq?

Groq provides fast inference, a free tier, and easy integration through a Python SDK.

### Why Flask?

Flask is lightweight, easy to deploy, and sufficient for the requirements of this project.


---

## Conclusion

The project successfully implemented a working RAG application capable of answering company policy questions with source citations. The system includes document ingestion, chunking, retrieval, LLM generation, automated testing, evaluation, and a web-based user interface.
