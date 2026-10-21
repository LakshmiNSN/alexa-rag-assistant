
from pathlib import Path
from pypdf import PdfReader

DOCUMENTS_DIR = Path(__file__).parent / "documents"


def load_documents():
    documents = []

    for file_path in DOCUMENTS_DIR.iterdir():
        if file_path.suffix.lower() == ".txt":
            text = file_path.read_text(encoding="utf-8")
            documents.append({
                "filename": file_path.name,
                "text": text
            })

        elif file_path.suffix.lower() == ".pdf":
            reader = PdfReader(str(file_path))
            text = "\n".join(
                page.extract_text() or ""
                for page in reader.pages
            )
            documents.append({
                "filename": file_path.name,
                "text": text
            })

    return documents


if __name__ == "__main__":
    docs = load_documents()

    for doc in docs:
        print(f"\nDocument: {doc['filename']}")
        print(doc["text"])

    print(f"\nTotal documents loaded: {len(docs)}")
