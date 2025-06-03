import faiss
import pickle
import numpy as np
from app.models.semantic_recommender_model import get_embedding
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
FAISS_INDEX_PATH = os.path.join(BASE_DIR, "faiss_index", "product_index.faiss")
PRODUCT_ID_MAP_PATH = os.path.join(BASE_DIR, "faiss_index", "product_id_map.pkl")

# Load FAISS index and ID map
faiss_index = faiss.read_index(FAISS_INDEX_PATH)
with open(PRODUCT_ID_MAP_PATH, "rb") as f:
    product_ids = pickle.load(f)

def query_faiss_index(user_text, top_k=100, threshold=0.9, final_k=40):
    """
    Search FAISS index and return top `final_k` products that have similarity above `threshold`.
    """
    emb = get_embedding(user_text).cpu().numpy().reshape(1, -1).astype("float32")
    D, I = faiss_index.search(emb, top_k)

    # Convert FAISS distances (L2) to cosine similarity approximation
    cosine_scores = 1 - (D[0] / 2)

    results = []
    for idx, sim in zip(I[0], cosine_scores):
        if idx < len(product_ids) and sim >= threshold:
            results.append((product_ids[idx], float(sim)))

    # Sort by similarity score and return only IDs
    results = sorted(results, key=lambda x: x[1], reverse=True)[:final_k]
    return [pid for pid, score in results]
