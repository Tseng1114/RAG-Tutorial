import os
import glob
import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter
import config

def load_and_split_pdf(directory):
    all_chunks = []
    file_pattern = os.path.join(directory, "*.pdf")
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.chunk_size, 
        chunk_overlap=config.chunk_overlap
    )

    for file_path in glob.glob(file_pattern):
        file_name = os.path.basename(file_path) 
        print(f"reading: {file_name}")
        doc = fitz.open(file_path)
        full_text = "".join([page.get_text() for page in doc])
        
        chunks = splitter.split_text(full_text)

        for content in chunks:
            all_chunks.append({
                "content": content,
                "source": file_name
            })
        doc.close()
        
    return all_chunks 