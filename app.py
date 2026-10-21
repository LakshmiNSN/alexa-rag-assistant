
from flask import Flask, request, jsonify
from semantic_search import semantic_search

app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>Hello, Alexa+ RAG Assistant!</h1>"


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

        # Avoid returning unrelated document content.
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
