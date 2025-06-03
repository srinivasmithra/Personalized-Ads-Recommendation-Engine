import os
import faiss
import pickle
import numpy as np
from tqdm import tqdm
from app.db.mongo_methods import fetch_documents
from app.models.semantic_recommender_model import get_embedding, embed_product

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
FAISS_DIR = os.path.join(BASE_DIR, "faiss_index")
FAISS_INDEX_PATH = os.path.join(FAISS_DIR, "product_index.faiss")
PRODUCT_ID_MAP_PATH = os.path.join(FAISS_DIR, "product_id_map.pkl")

def build_faiss_index():
    os.makedirs(FAISS_DIR, exist_ok=True)

    product_cursor = fetch_documents("products")
    product_embeddings = []
    product_ids = []

    for product in tqdm(product_cursor, desc="Encoding products"):
        text = embed_product(product)
        emb = get_embedding(text).cpu().numpy()
        product_embeddings.append(emb)
        product_ids.append(str(product["_id"]))

    if not product_embeddings:
        print("No products to index.")
        return

    dim = product_embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(product_embeddings).astype("float32"))

    # Save index and ID map
    faiss.write_index(index, FAISS_INDEX_PATH)
    with open(PRODUCT_ID_MAP_PATH, "wb") as f:
        pickle.dump(product_ids, f)

if __name__ == "__main__":
    build_faiss_index()
