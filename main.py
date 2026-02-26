import requests
from google import genai
import config
from documents_loader import load_documents
from text_splitter import split_documents
from vector_database import VectorEngine
from prompts import get_rag_prompt

def call_local(prompt: str) -> str:
    url = f"{config.ollama_base_url}/api/generate"
    payload = {
        "model": config.LOCAL_MODEL,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, json=payload, timeout=120)
    response.raise_for_status()
    return response.json()["response"]


def call_api(prompt: str) -> str:
    client = genai.Client(api_key=config.llm_API_key)
    response = client.models.generate_content(
        model=config.API_MODEL,
        contents=prompt
    )
    return response.text


def get_llm_response(prompt: str) -> str:
    if config.LLM_MODE == "local":
        return call_local(prompt)
    else:
        return call_api(prompt)


def main():
    if config.LLM_MODE == "local":
        print(f"LLM Mode: Local -- ({config.LOCAL_MODEL})")
    else:
        print(f"LLM Mode: API --({config.API_MODEL})")

    vector_engine = VectorEngine()

    if not vector_engine.load_index():
        print("First run, processing files...")
        raw_docs = load_documents(config.data_path)

        if not raw_docs:
            print("Check file path setting or make sure supported files exist.")
            return

        docs = split_documents(raw_docs)
        vector_engine.build_index(docs)
    else:
        print("Index loading successful, skipping file processing.")

    print("\n" + "==" * 30)
    print("Ready! You can ask any questions now.")
    print("Enter 'exit' or 'quit' to end this conversation.")
    print("==" * 30 + "\n")

    while True:
        user_query = input("\nEnter your question: ").strip()

        if user_query.lower() in ['exit', 'quit']:
            print("See you next time!")
            break

        if not user_query:
            continue

        try:
            print("Retrieving relevant information...")
            context = vector_engine.search(user_query)
            final_prompt = get_rag_prompt(context, user_query)

            print("Generating answer...")
            answer = get_llm_response(final_prompt)

            print(f"\nAnswer:\n{answer}")
            print("\n" + "**" * 20)

        except requests.exceptions.ConnectionError:
            print("Error: Unable to connect to Ollama. Please check that Ollama is running (ollama serve).")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()