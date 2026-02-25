import faiss
import pickle
import os
import numpy as np
from sentence_transformers import SentenceTransformer
import config


class VectorEngine:
    def __init__(self):
        self.model_name = config.embedding_model_name.lower()

        self.is_e5 = "e5" in self.model_name
        self.is_nomic = "nomic" in self.model_name
        self.is_bge = "bge" in self.model_name

        model_folder = self.model_name.replace("/", "_")
        self.db_dir = os.path.join(config.vector_index_dir, model_folder)
        self.index_path = os.path.join(self.db_dir, "vector.index")
        self.pickle_path = os.path.join(self.db_dir, "chunks.pkl")

        os.makedirs(self.db_dir, exist_ok=True)

        print(f" Loading embedding model: {self.model_name}")

        self.embed_model = SentenceTransformer(
            self.model_name,
            trust_remote_code=self.is_nomic
        )

        self.index = None
        self.documents = []

    def load_index(self):
        if os.path.exists(self.index_path) and os.path.exists(self.pickle_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.pickle_path, "rb") as f:
                self.documents = pickle.load(f)
            print("Index loaded")
            return True
        return False

    def build_index(self, docs):
        if not docs:
            raise ValueError("Document list is empty")

        self.documents = docs

        if self.is_e5:
            texts = [f"passage: {d['content']}" for d in docs]
        else:
            texts = [d["content"] for d in docs]

        print(f" Encoding {len(texts)} documents...")

        embeddings = self.embed_model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True,
            normalize_embeddings=True
        ).astype("float32")

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)

        faiss.write_index(self.index, self.index_path)
        with open(self.pickle_path, "wb") as f:
            pickle.dump(self.documents, f)

        print("Index built & saved")

    def search(self, query, k=config.top_k):
        if self.index is None:
            raise ValueError("Index not loaded")

        if self.is_e5:
            query = f"query: {query}"

        query_vec = self.embed_model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        ).astype("float32")

        distances, indices = self.index.search(query_vec, k)

        results = []

        for idx in indices[0]:
            if idx == -1:
                continue

            doc = self.documents[idx]
            results.append(doc["content"])

        return "\n-----\n".join(results)