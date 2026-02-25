import os
from dotenv import load_dotenv

load_dotenv()

base_dir = os.path.dirname(os.path.abspath(__file__))
vector_index_dir = os.path.join(base_dir, "vector_index")
gemini_API_key = os.getenv("GEMINI_API_KEY")


data_folder = os.getenv("DATA_DIR_NAME", "test_file")
data_path = os.path.join(base_dir, data_folder)
faiss_index_path = os.path.join(vector_index_dir, "faiss_index.bin")
documents_pickle_path = os.path.join(vector_index_dir, "documents.pkl")

gemini_model_name = "gemini-2.5-flash"
# LLM = gemini-2.5-pro, gemini-2.5-flash

embedding_model_name = 'BAAI/bge-m3'
# embedding models = BAAI/bge-m3, nomic-ai/nomic-embed-text-v1.5, intfloat/multilingual-e5-small
chunk_size = 500
chunk_overlap = 50

top_k = 5