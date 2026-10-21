
from pathlib import Path

import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Alexa RAG Assistant")

DOCUMENTS_DIR = Path(__file__).parent / "documents"
FLASK_ASK_URL = "http://127.0.0.1:5000/ask"


@mcp.tool()
def search_knowledge(query: str) -> str:
    """Search local text documents for relevant information."""
    if not query.strip():
        return "Please enter a search query."

    if not DOCUMENTS_DIR.exists():
        return "Documents folder not found."

    results = []

    for file_path in DOCUMENTS_DIR.glob("*.txt"):
        try:
            text = file_path.read_text(encoding="utf-8")
            for paragraph in text.split("\n\n"):
                if query.lower() in paragraph.lower():
                    results.append(
                        f"Source: {file_path.name}\n{paragraph.strip()}"
                    )
        except OSError:
            continue

    if results:
        return "\n\n".join(results)

    return "No exact text match found in the documents."


@mcp.tool()
def ask_about_project() -> str:
    """Return information about this assistant."""
    return (
        "I am Alexa+ RAG Assistant, a project using "
        "Python, Gemini, and MCP."
    )


@mcp.tool()
def ask_documents(question: str) -> str:
    """Send a question to the Flask document-question endpoint."""
    if not question or not question.strip():
        return "Please enter a question."

    try:
        response = requests.post(
            FLASK_ASK_URL,
            json={"question": question},
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("answer", "No answer returned by Flask.")

    except requests.RequestException as error:
        return f"Could not reach the Flask app: {error}"
    except ValueError:
        return "The Flask app returned an invalid JSON response."


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
