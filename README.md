# BrightWave Policy Assistant (RAG Application)

## Overview

BrightWave Policy Assistant is a Retrieval-Augmented Generation (RAG) application that answers questions about company policies and procedures.

The system retrieves relevant policy content from a corpus of company documents and uses a Large Language Model (LLM) to generate answers with citations.

---

## Features

* Company policy question answering
* Retrieval-Augmented Generation (RAG)
* Source citations
* Flask web interface
* JSON API endpoint
* Health check endpoint
* Automated testing with pytest
* GitHub Actions CI workflow

---

## Project Structure

```text
company-policy-rag/
├── .github/
│   └── workflows/
│       └── ci.yml
├── data/
│   ├── policies/
│   └── evaluation_questions.json
├── src/
│   ├── ingest.py
│   ├── chunking.py
│   ├── retrieval.py
│   ├── rag.py
│   └── evaluate.py
├── tests/
│   └── test_app.py
├── app.py
├── requirements.txt
├── README.md
├── design-and-evaluation.md
└── ai-tooling.md
```

---

## Setup

### Clone Repository

```bash
git clone <repository-url>
cd company-policy-rag
```

### Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root:

```text
GROQ_API_KEY=your_groq_api_key
```

---

## Running the Application

Start the Flask application:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

in a browser.

---

## API Endpoints

### Home Page

```text
GET /
```

Returns the web-based chat interface.

### Chat Endpoint

```text
POST /chat
```

Example request:

```json
{
  "question": "How many PTO days do employees receive?"
}
```

Example response:

```json
{
  "question": "How many PTO days do employees receive?",
  "answer": "Employees receive 20 days of PTO per calendar year.",
  "sources": [...]
}
```

### Health Check

```text
GET /health
```

Example response:

```json
{
  "status": "ok"
}
```

---

## Running Tests

```bash
pytest
```

---

## Running Evaluation

```bash
python src/evaluate.py
```

This executes the evaluation dataset and reports latency metrics.

---

## Technologies Used

* Python 3.11
* Flask
* Groq API
* Llama 3.1 8B Instant
* Pytest
* GitHub Actions

---

## Author

Laura Weaver
