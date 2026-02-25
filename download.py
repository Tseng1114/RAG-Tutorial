from sentence_transformers import SentenceTransformer

def download_embedding_model1(): 
    model_name = "BAAI/bge-m3"
    try:
        model = SentenceTransformer(model_name)
        print(f"Download {model_name} successfully!")
    except Exception as e:
        print(f"Error: {e}")

def download_embedding_model2(): #pip install einops
    model_name = "nomic-ai/nomic-embed-text-v1.5"
    try:
        model = SentenceTransformer(model_name, trust_remote_code=True)
        print(f"Download {model_name} successfully!")
    except Exception as e:
        print(f"Error: {e}")

def download_embedding_model3():
    model_name = "intfloat/multilingual-e5-small"
    try:
        model = SentenceTransformer(model_name)
        print(f"Download {model_name} successfully!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
# Comment out the models you are not using.
# embedding model1 = BAAI/bge-m3
# embedding model2 = nomic-ai/nomic-embed-text-v1.5
# embedding model3 = intfloat/multilingual-e5-small
    download_embedding_model1()
    download_embedding_model2()
    download_embedding_model3()