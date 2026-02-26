import os
import glob
import fitz  # PyMuPDF


def load_documents(directory: str) -> list[dict]:
    """
    讀取指定資料夾內所有 PDF 檔案，回傳原始文件清單。
    每筆資料包含：
        - content: 整份 PDF 的文字內容
        - source:  檔案名稱
    """
    raw_docs = []
    file_pattern = os.path.join(directory, "*.pdf")
    pdf_files = glob.glob(file_pattern)

    if not pdf_files:
        print(f"No PDF files found in: {directory}")
        return raw_docs

    for file_path in pdf_files:
        file_name = os.path.basename(file_path)
        print(f"Reading: {file_name}")

        try:
            doc = fitz.open(file_path)
            full_text = "".join([page.get_text() for page in doc])
            doc.close()

            if full_text.strip():
                raw_docs.append({
                    "content": full_text,
                    "source": file_name
                })
            else:
                print(f"Warning: No text extracted from {file_name}, skipping.")

        except Exception as e:
            print(f"Error reading {file_name}: {e}")

    print(f"Loaded {len(raw_docs)} document(s).")
    return raw_docs
