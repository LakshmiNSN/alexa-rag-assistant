# Alexa+ RAG Assistant

A Python-based question-answering assistant that searches existing project documents and returns answers with source filenames. It also exposes tools through the Model Context Protocol (MCP).

Built for the Build, Ship, Shape: Amazon Developer Hackathon 2026 — Alexa+ track.

## Features

- Ask questions through a Flask web interface.
- Search existing project documents.
- Retrieve relevant text using semantic search.
- Return answers based on retrieved document content.
- Display source filenames in search results.
- Provide a fallback response when relevant information is not found.
- Expose three MCP tools:
  - `ask_about_project`
  - `search_knowledge`
  - `ask_documents`

## Architecture

- Browser UI → Flask application (`app.py`) → `semantic_search.py`
- MCP client → MCP server (`mcp_server.py`) → Flask `/ask` endpoint

## Technologies

- Python
- Flask
- FastEmbed
- NumPy
- Google GenAI SDK
- Model Context Protocol (MCP)
- pypdf dependency

## Requirements

- Windows 10 or 11
- Python 3.10 or newer
- Git
- Google Gemini API key if required by the configured application

## Installation

Clone the repository:

```powershell
git clone https://github.com/LakshmiNSN/alexa-rag-assistant.git
cd alexa-rag-assistant
```

Create a virtual environment and activate it:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
py -m pip install -r requirements.txt
```

## Configuration

Configure your Gemini API key if required by the application.

Keep secret keys in a local environment file and never commit real API keys to GitHub.

## Usage

Start the Flask application:

```powershell
py app.py
```

Open http://127.0.0.1:5000 in your browser.

In a second terminal, start the MCP server:

```powershell
py mcp_server.py
```

MCP endpoint: http://127.0.0.1:8000/mcp

Keep both servers running for the tested MCP workflow.

## Testing

Run the MCP test script:

```powershell
py test_mcp.py
```

### Tests completed

- Tested the Flask question-answering interface.
- Verified answers to relevant document questions.
- Verified the fallback response for an unsupported question.
- Started the MCP server successfully.
- Ran `test_mcp.py` successfully.
- Verified the tools `ask_about_project`, `search_knowledge`, and `ask_documents`.

## Known Limitations

- The current web interface searches existing documents; document upload has not been verified.
- Answers depend on the retrieved document content.
- Both the Flask application and MCP server must be running for the tested MCP workflow.
- Authentication and per-user document separation have not been verified.
- Direct Alexa+ device integration has not been verified.

## License

MIT License. See the `LICENSE` file for details.
