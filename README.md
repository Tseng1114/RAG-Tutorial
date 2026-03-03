# Quickstart

1. Install dependencies
```
pip install -r requirements.txt
```

2. Set up `.env`

create a `.env` file in the project root directory:

```
#Gemini
LLM_API_KEY=your_api_key
#Groq     
LLM_API_KEY_groq=your_api_key
#GitHub
LLM_github_token=your_access_token
DATA_PATH=test_file          #path to your documents
```

3.  Place your documents

put your files into the `test_file` folder (or whichever folder you set in DATA_PATH).

4. Run `download.py` if you haven't downloaded an embedding model yet.
```
python download.py
```
5. Configure `config.py`
```
LLM_MODE = "local"                                      # "local" or "api"
API_TYPE = "github"                                     # if you choose api, specify "gemini", "groq" or "github"
LOCAL_MODEL = "llama3.2"                                # e.g. llama3.2, qwen2.5, gemma2, phi3.5
API_MODEL_gemini = "gemini-2.5-flash"                   # e.g. gemini-2.5-flash、gemini-2.5-pro
API_MODEL_groq = "llama-3.3-70b-versatile"              # e.g. llama-3.3-70b-versatile、mixtral-8x7b-32768、gemma2-9b-it、meta-llama/llama-4-scout-17b-16e-instruct
API_MODEL_github_model = "gpt-4o"                       # e.g. gpt-4o、o1-mini
                        
embedding_model_name = "intfloat/multilingual-e5-small" # e.g. BAAI/bge-m3, nomic-ai/nomic-embed-text-v1.5

# Chunking & retrieval settings
chunk_size = 500
chunk_overlap = 50
top_k = 5 
```

6. Run
```
python main.py
```
# Notice
While `main.py` is running, you can use the following commands :
* `exit` or `quit`:
  Ends the current session and safely exits the program.
* `quota`:
  Checks the usage status of the API provider:
  * **Groq**: Displays **RPM** and **TPM**, also rate limit descriptions.
  * **Gemini / GitHub Models**: Only provides rate limit descriptions. 
3. The vector index is cached in vector_index/. If you add or change documents, delete the index folder and re-run
# Architecture diagram
```mermaid
flowchart LR
subgraph INPUT ["Input Documents"]
  direction TB
  i1["PDF"]
  i2["DOCX"]
  i3["PPTX"]
  i4["XLSX"]
  i5["CSV"]
  i6["TXT"]
end

    subgraph LOAD ["Indexing"]
      direction LR
      B["Document Loader"]
      C["Text Splitter"]
      subgraph D["Embedding model"]
        direction LR
        A1["bge-m3"]
        A2["nomic-embed-text-v1.5"]
        A3["multilingual-e5-small"]
        A4["..."]
      end
    subgraph E ["Vector Index"]
    direction LR
    V1["FAISS"]
    V2["..."]
    end   
    B --> C --> D --> E
    end

    subgraph QUERY ["Querying"]
      direction LR
      F["User Query"]
      G["Query Embedding"]
      H["Similarity Search<br/>Top-K Retrieval"]
      I["Prompt Template"]
      J{"LLM_MODE"}
      subgraph LOCAL ["Local - Ollama"]
        direction TB
        K1["llama3.2"]
        K2["qwen2.5"]
        K3["gemma2"]
        K4["phi3.5"]
        K5["..."]
      end
      subgraph API ["API"]
        direction TB
        K6["gemini-2.5-flash"]
        K7["gemini-2.5-pro"]
        K8["..."]
      end  
      M["Answer"]
      F --> G --> H --> I --> J
      J -->|local| LOCAL --> M
      J -->|api| API --> M
    end

    INPUT --> B
    E -->|load index| H
```
# Flowchart
```mermaid
flowchart TD
    A([Start]) --> B[Configure relevant settings]
    B --> C[Initialize VectorEngine and load embedding model]
    C --> D{Does the vector index exist?}

    D -- No --> E[load_documents]
    E --> F{detect file extension<br/>.pdf / .docx / .pptx / <br/> .xlsx / .csv / .txt}
    F --> G[Corresponding Loader parses text]
    G --> H[split_documents]
    H --> I[build_index<br/>SentenceTransformer encoding]
 
    I --> K[store index <br/>in chunks.pkl]
    K --> L

    D -- Yes --> L[Load index]

    L --> M([Ready])

    M --> N[user_query]
    N --> O{exit or quit？}
    O -- Yes --> P([Finish])
    O --No --> Q[search</br>top-K similarity Search]
    Q --> R[get_rag_prompt</br> Combine context and query]
    R --> S{LLM mode}
    S -- LOCAL --> T[get_llm_response<br/>call_local]
    S -- API --> U[get_llm_response<br/>call_api]
    T --> V[Answer]
    U --> V
    V --> N

    style A fill:#4F46E5,color:#fff
    style M fill:#059669,color:#fff
    style P fill:#DC2626,color:#fff
    style D fill:#D97706,color:#fff
    style F fill:#D97706,color:#fff
    style O fill:#D97706,color:#fff
    style S fill:#D97706,color:#fff
```
