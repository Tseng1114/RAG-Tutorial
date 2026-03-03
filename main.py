import requests
from google import genai
from groq import Groq
import openai
import config
from documents_loader import load_documents
from text_splitter import split_documents
from vector_database import VectorEngine
from prompts import get_rag_prompt
from token_quota_check import token_usage_groq,token_usage_gemini,token_usage_github_models

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
    if config.API_TYPE == "gemini":
        client = genai.Client(api_key=config.llm_API_key_gemini)
        response = client.models.generate_content(
            model=config.API_MODEL_gemini,
            contents=prompt
        )
        return response.text
    elif config.API_TYPE == "groq":
        client = Groq(api_key=config.llm_API_key_groq)
        completion = client.chat.completions.create(
            model=config.API_MODEL_groq,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return completion.choices[0].message.content
    elif config.API_TYPE == "github":
        client = openai.OpenAI(
            base_url="https://models.github.ai/inference",
            api_key=config.llm_github_models_token,
        )
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=config.API_MODEL_github_model,
            temperature=0.7,
        )
        return response.choices[0].message.content
    else:
        raise ValueError("Invalid API type specified.")


def get_llm_response(prompt: str) -> str:
    if config.LLM_MODE == "local":
        return call_local(prompt)
    else:
        return call_api(prompt)


def main():
    if config.LLM_MODE == "local":
        print(f"LLM Mode: Local -- ({config.LOCAL_MODEL})")
    elif config.LLM_MODE == "api" and config.API_TYPE == 'groq':
        print(f"LLM Mode: API --({config.API_MODEL_groq})")
    elif config.LLM_MODE == "api" and config.API_TYPE == 'gemini':
        print(f"LLM Mode: API --({config.API_MODEL_gemini})")
    elif config.LLM_MODE == "api" and config.API_TYPE == 'github':
        print(f"LLM Mode: API --({config.API_MODEL_github_model})")

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
    print("Enter quota to check your quoto.")
    print("==" * 30 + "\n")

    while True:
        user_query = input("\nEnter your question: ").strip()

        if user_query.lower() in ['exit', 'quit']:
            print("See you next time!")
            break
        if user_query.lower() in ['quota']:
            if(config.API_TYPE == 'groq'):
                token_usage_groq()
                continue
            elif(config.API_TYPE == 'gemini'):
                token_usage_gemini()
                continue
            elif(config.API_TYPE == 'github'):
                token_usage_github_models()
                continue            
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