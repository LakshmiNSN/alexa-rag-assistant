
from fastembed import TextEmbedding
from load_documents import load_documents

def semantic_search(query: str, top_k: int = 3):
    docs = load_documents()

    if not docs:
        return []

    model = TextEmbedding()

    paragraphs = []
    for doc in docs:
        for paragraph in doc["text"].split("\n\n"):
            paragraph = paragraph.strip()
            if paragraph:
                paragraphs.append({
                    "filename": doc["filename"],
                    "text": paragraph
                })

    if not paragraphs:
        return []

    query_embedding = list(model.embed([query]))[0]
    document_embeddings = list(
        model.embed([item["text"] for item in paragraphs])
    )

    def cosine_similarity(a, b):
        dot = sum(float(x) * float(y) for x, y in zip(a, b))
        norm_a = sum(float(x) ** 2 for x in a) ** 0.5
        norm_b = sum(float(y) ** 2 for y in b) ** 0.5
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    results = []
    for item, embedding in zip(paragraphs, document_embeddings):
        score = cosine_similarity(query_embedding, embedding)
        results.append({
            "filename": item["filename"],
            "text": item["text"],
            "score": score
        })

    results.sort(key=lambda item: item["score"], reverse=True)
    return results[:top_k]


if __name__ == "__main__":
    question = input("Enter your search question: ")
    matches = semantic_search(question)

    if matches:
        for match in matches:
            print(f"\nSource: {match['filename']}")
            print(f"Similarity: {match['score']:.3f}")
            print(match["text"])
    else:
        print("No documents available to search.")
