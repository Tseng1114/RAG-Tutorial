# Quickstart

1. Install dependencies
```
pip install -r requirements.txt
```

2. Set up `.env`

create a `.env` file in the project root directory: <br>
```
LLM_API_KEY=your_api_key     #gemini, ...
DATA_PATH=test_file          #path to your documents
```

3.  Place your documents

put your files into the test_file folder (or whichever folder you set in DATA_PATH).

4. Run 'download.py' if you haven't downloaded an embedding model yet
```
python download.py
```
5. Configure `config.py`
```
LLM_MODE = "local"                                      # "local" or "api"
LOCAL_MODEL = "llama3.2"                                # e.g. llama3.2, qwen2.5, gemma2, phi3.5
API_MODEL = "gemini-2.5-flash"                          # e.g. gemini-2.5-flash, gemini-2.5-pro
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

The vector index is cached in vector_index/. If you add or change documents, delete the index folder and re-run
# Flowchart
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
