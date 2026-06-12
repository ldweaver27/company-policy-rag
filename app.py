from flask import Flask, jsonify, request, render_template_string
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "src"))

from rag import answer_question


app = Flask(__name__)


HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>BrightWave Policy Assistant</title>
</head>
<body>
    <h1>BrightWave Policy Assistant</h1>
    <p>Ask a question about company policies.</p>

    <form method="post" action="/chat-form">
        <input type="text" name="question" style="width: 500px;" placeholder="How many PTO days do employees receive?">
        <button type="submit">Ask</button>
    </form>

    {% if question %}
        <h2>Question</h2>
        <p>{{ question }}</p>

        <h2>Answer</h2>
        <p>{{ answer }}</p>

        <h2>Sources</h2>
        <ul>
        {% for source in sources %}
            <li>{{ source.title }} - {{ source.source }}</li>
        {% endfor %}
        </ul>
    {% endif %}
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML_PAGE)


@app.route("/chat-form", methods=["POST"])
def chat_form():
    question = request.form.get("question", "")
    result = answer_question(question)

    return render_template_string(
        HTML_PAGE,
        question=result["question"],
        answer=result["answer"],
        sources=result["sources"],
    )


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("question", "")

    result = answer_question(question)

    return jsonify({
        "question": result["question"],
        "answer": result["answer"],
        "sources": [
            {
                "title": source["title"],
                "source": source["source"],
                "snippet": source["text"][:300]
            }
            for source in result["sources"]
        ]
    })


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)