
from flask import Flask, request, jsonify, render_template_string
from semantic_search import semantic_search

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alexa+ RAG Assistant</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 700px;
            margin: 40px auto;
            padding: 20px;
            background: #f4f6f8;
        }
        main {
            background: white;
            padding: 24px;
            border-radius: 12px;
        }
        input, button {
            box-sizing: border-box;
            width: 100%;
            padding: 12px;
            margin: 8px 0;
        }
        button {
            background: #1769aa;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
        }
        #result {
            white-space: pre-wrap;
            overflow-wrap: anywhere;
            margin-top: 20px;
        }
    </style>
</head>
<body>
<main>
    <h1>Alexa+ RAG Assistant</h1>
    <p>Ask questions about your indexed documents.</p>

    <form id="ask-form">
        <label for="question">Your question</label>
        <input id="question" name="question"
               placeholder="What is this document about?" required>
        <button type="submit">Ask Question</button>
    </form>

    <div id="result" role="status"></div>
</main>

<script>
document.getElementById("ask-form").addEventListener("submit",
    async function(event) {
        event.preventDefault();

        const result = document.getElementById("result");
        const question = document.getElementById("question").value.trim();

        result.textContent = "Searching documents...";

        try {
            const response = await fetch("/ask", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({question: question})
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Request failed.");
            }

            result.textContent =
                "Answer: " + data.answer +
                "\\n\\nSources: " +
                (data.sources.length ? data.sources.join(", ") : "None found");
        } catch (error) {
            result.textContent = "Error: " + error.message;
        }
    }
);
</script>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML_PAGE)


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip()

    if not question:
        return jsonify({
            "error": "No question was provided."
        }), 400

    try:
        results = semantic_search(question, top_k=3)

        if not results:
            return jsonify({
                "question": question,
                "answer": "I couldn't find relevant information in the documents.",
                "sources": [],
                "status": "success"
            })

        best_match = results[0]

        if best_match["score"] < 0.50:
            return jsonify({
                "question": question,
                "answer": "I couldn't find relevant information in the documents.",
                "sources": [],
                "status": "success"
            })

        answer = best_match["text"]
        sources = list(dict.fromkeys(
            result["filename"] for result in results
            if result["score"] >= 0.35
        ))

        return jsonify({
            "question": question,
            "answer": answer,
            "sources": sources,
            "status": "success"
        })

    except Exception:
        app.logger.exception("Document search failed")
        return jsonify({
            "error": "Document search failed. Check the terminal for details."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
