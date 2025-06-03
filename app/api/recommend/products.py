from fastapi import APIRouter, Depends
from app.api.auth.deps import get_current_user
from app.test_models.transformers_recommender import get_cls_embedding
from app.db.mongo_methods import fetch_documents
from random import shuffle
from collections import defaultdict

router = APIRouter(prefix="/recommend", tags=["recommend"])

@router.get("/")
def get_recommendations(user=Depends(get_current_user)):
    interests = user.get("interests", [])
    search_history = user.get("search_history", [])
    keywords = list(set(interests + search_history))

    product_cursor = fetch_documents("products")
    all_products = [p for p in product_cursor]

    buckets = defaultdict(list)
    for keyword in keywords:
        keyword_emb = get_cls_embedding(keyword)
        for product in all_products:
            prod_text = product.get("name", "") + " " + product.get("tags", "")
            prod_emb = get_cls_embedding(prod_text)
            score = (keyword_emb @ prod_emb.T).item()
            buckets[keyword].append((product, score))

    combined = []
    for key, items in buckets.items():
        items.sort(key=lambda x: x[1], reverse=True)
        combined.extend(items[:10])  # Top 10 per interest

    seen = set()
    diverse_products = []
    for product, score in combined:
        pid = str(product.get("_id"))
        if pid not in seen:
            diverse_products.append(product)
            seen.add(pid)

    shuffle(diverse_products)
    return {"recommendations": diverse_products[:30]}  # limit to 30 results
