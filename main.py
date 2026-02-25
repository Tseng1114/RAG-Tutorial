from google import genai
import config
from text_splitter import load_and_split_pdf
from vector_database import VectorEngine
from prompts import get_rag_prompt

def main():
    client = genai.Client(api_key=config.gemini_API_key)
    vector_engine = VectorEngine()
    docs = load_and_split_pdf(config.data_path)
    
    if not docs:
        print("Check file path setting")
        return

    vector_engine.build_index(docs)
    if not vector_engine.load_index():
        print("First run, processing files...")
        docs = load_and_split_pdf(config.data_path)
        vector_engine.build_index(docs)
    else:
        print("Index loading successful, skip the file processing.")
    print("\n" + "=="*30)
    print("File processing complete. You can ask any questions now.")
    print("or enter 'exit'/'quit' to end this conversation.")
    print("=="*30 + "\n")

    while True:
        user_query = input("\nEnter your question：").strip()

        if user_query.lower() in ['exit', 'quit']:
            print("See you next time！")
            break
        
        if not user_query:
            continue

        try:
            print("Retrieving relevant information...")
            context = vector_engine.search(user_query)
            final_prompt = get_rag_prompt(context, user_query)

            response = client.models.generate_content(
                model=config.gemini_model_name,
                contents=final_prompt
            )

            print(f"\nAnswer：\n{response.text}")
            print("\n" + "**"*20)

        except Exception as e:
            print(f"Error：{e}")

if __name__ == "__main__":
    main()