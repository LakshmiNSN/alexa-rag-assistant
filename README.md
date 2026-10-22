# Alexa+ RAG Assistant

A Python-based document question-answering assistant that retrieves relevant information from project documents and returns answers with source filenames. It also exposes question-answering functionality through an MCP server.

Built for the **Build, Ship, Shape: Amazon Developer Hackathon 2026 — Alexa+ track**.

## Features

- Ask questions through a Flask web interface.
- Search existing project documents for relevant information.
- Retrieve relevant document text using semantic search.
- Return answers based on retrieved document content.
- Display source filenames in search results.
- Provide a fallback response when relevant information is not found.
- Expose three MCP tools:
  - `ask_about_project`
  - `search_knowledge`
  - `ask_documents`

## Architecture

Browser UI → Flask application (`app.py`) → `semantic_search.py`

MCP client → MCP server (`mcp_server.py`) → Flask `/ask` endpoint

The project dependencies include:

- **Python** — application logic
- **Flask** — web interface and question-answering endpoint
- **FastEmbed** — local text embeddings
- **NumPy** — numerical operations for similarity search
- **Google GenAI SDK** — Gemini API integration
- **MCP** — exposes project tools to compatible clients
- **pypdf** — PDF text extraction dependency

## Requirements

- Windows 10 or Windows 11
- Python 3.10 or newer
- Git
- Google Gemini API key, if using Gemini-powered functionality

## Installation

Clone the repository:

```powershell
git clone https://github.com/LakshmiNSN/alexa-rag-assistant.git
cd alexa-rag-assistant
```

Create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
py -m pip install -r requirements.txt
```

## Configuration

If Gemini-powered functionality is required, configure your API key using the environment-variable method supported by your application.

Example:

```ini
GEMINI_API_KEY=your_key_here
```

Never commit your actual API key or other secrets to GitHub.

## Usage

### 1. Start the Flask application

Open a terminal in the project directory and run:

```powershell
py app.py
```

Open the web interface:

http://127.0.0.1:5000

Enter a question about the existing project documents and click the question button.

### 2. Start the MCP server

Open a second terminal in the project directory, activate the virtual environment, and run:

```powershell
.\.venv\Scripts\Activate.ps1
py mcp_server.py
```

MCP endpoint:

http://127.0.0.1:8000/mcp

Keep both servers running when testing the MCP tools.

## Testing

Run the MCP test script from another terminal:

```powershell
py test_mcp.py
```

### Tests completed

- Flask question-answering interface tested.
- Relevant document questions returned answers and source filenames.
- Unsupported questions returned a fallback response.
- MCP server started successfully.
- `test_mcp.py` completed successfully.
- Verified the following MCP tools:
  - `ask_about_project`
  - `search_knowledge`
  - `ask_documents`

## Known Limitations

- The current web interface searches existing project documents; document upload has not been verified.
- Answers depend on the information retrieved from the available documents.
- Both the Flask application and MCP server must be running for the tested MCP workflow.
- Authentication and per-user document separation have not been implemented or verified.
- Direct Alexa+ device integration has not been verified.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
