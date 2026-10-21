
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)


def ask_gemini(question: str) -> str:
    response = client.interactions.create(
        model="gemini-3.8-flash",
        input=question,
    )
    return response.output_text


if __name__ == "__main__":
    question = input("Ask your Alexa+ RAG Assistant: ")
    answer = ask_gemini(question)
    print("\nGemini:", answer)

