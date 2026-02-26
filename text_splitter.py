from langchain_text_splitters import RecursiveCharacterTextSplitter
import config


def split_documents(raw_docs: list[dict]) -> list[dict]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap
    )

    all_chunks = []

    for doc in raw_docs:
        chunks = splitter.split_text(doc["content"])
        for chunk_text in chunks:
            all_chunks.append({
                "content": chunk_text,
                "source": doc["source"]
            })

    print(f"Split into {len(all_chunks)} chunk(s).")
    return all_chunks
