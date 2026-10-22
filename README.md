
# Alexa+ RAG Assistant

Upload documents, ask questions, and receive answers grounded in your files with source citations. The question-answering feature is also available as an MCP tool.

Built for the Build, Ship, Shape: Amazon Developer Hackathon 2026 (Alexa+ track).

## Features

- Upload PDF, TXT and Markdown files
- Extract text and split documents into chunks
- Generate local embeddings using FastEmbed
- Retrieve relevant document chunks using cosine similarity
- Generate answers using Google Gemini
- Provide source citations from retrieved documents
- MCP tool named `ask_documents`

## Architecture

Browser UI → Flask app (`app.py`) → RAG pipeline (`rag.py`)

The RAG pipeline uses:
- pypdf for PDF text extraction
- FastEmbed for embeddings
- NumPy for similarity search
- Google Gemini API for answer generation

MCP client → `mcp_server.py` → Flask `/ask` endpoint

## Requirements

- Windows 10/11
- Python 3.10 or newer
- Google Gemini API key

## Installation

```powershell
git clone https://github.com/YOUR-USERNAME/alexa-rag-assistant.git
cd alexa-rag-assistant
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

## Configuration

Create a `.env` file based on `.env.example` and add your Gemini API key.

```ini
GEMINI_API_KEY=your_key_here
```

Never commit `.env` to GitHub.

## Usage

Start the Flask application:

```powershell
py app.py
```

Open http://127.0.0.1:5000 in your browser.

Start the MCP server in a second terminal:

```powershell
py mcp_server.py
```

MCP endpoint: http://127.0.0.1:8000/mcp

## Testing

Run the test script with both servers running:

```powershell
py test_mcp.py
```

Test results: Add your actual test results here.

## Known Limitations

- Documents are stored in memory and lost when the web app restarts.
- Scanned PDFs without extractable text are not supported.
- Both the Flask app and MCP server must be running for MCP requests.
- No authentication or per-user document separation.
- Alexa+ integration status: Describe what you actually tested.

## License

MIT License. See the `LICENSE` file.
