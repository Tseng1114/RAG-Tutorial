import os
from dotenv import load_dotenv

load_dotenv()

base_dir = os.path.dirname(os.path.abspath(__file__))
vector_index_dir = os.path.join(base_dir, "vector_index")

LLM_MODE = "api"   # "local" or "api"
API_TYPE = "github"  # if you choose api, specify "gemini", "groq" or "github"

#If you choose "local", specify the model you have downloaded(ollama pull LLM_NAME):
LOCAL_MODEL = "llama3.2"
#llama3.2、qwen2.5、gemma2、phi3.5

#If you choose "api", specify the model name and API key:
API_MODEL = "gpt-4o"
#gemini: gemini-2.5-flash、gemini-2.5-pro
#groq: llama-3.3-70b-versatile、mixtral-8x7b-32768、gemma2-9b-it、meta-llama/llama-4-scout-17b-16e-instruct
#github: gpt-4o、claude-3-5-sonnet、o1-mini

#Choose your embedding model, you can run download.py to download the model
embedding_model_name = "intfloat/multilingual-e5-small"
#BAAI/bge-m3、nomic-ai/nomic-embed-text-v1.5、intfloat/multilingual-e5-small

#Chunking & retrieval settings
chunk_size = 500
chunk_overlap = 50
top_k = 5


data_folder = os.getenv("DATA_PATH", "test_file")
data_path = os.path.join(base_dir, data_folder)

faiss_index_path = os.path.join(vector_index_dir, "faiss_index.bin")
documents_pickle_path = os.path.join(vector_index_dir, "documents.pkl")

llm_API_key_gemini = os.getenv("LLM_API_KEY_gemini")
llm_API_key_groq = os.getenv("LLM_API_KEY_groq")
llm_github_token = os.getenv("LLM_github_token")
ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
