from fastapi import APIRouter, Depends, Query, BackgroundTasks
from bson import ObjectId
from random import shuffle
from datetime import datetime

from app.db.mongo_connection import db
from app.db.mongo_methods import fetch_documents, update_document
from app.api.auth.deps import get_current_user
from app.db.collection_names import collections
from app.models.helper.ann_recommender import query_faiss_index
from app.models.semantic_recommender_model import (embed_user)

router = APIRouter(prefix="/recommend", tags=["recommend"])


def format_photo(photo):
    return {
        "alt": photo.get("alt"),
        "category": photo.get("category"),
        "photographer": photo.get("photographer"),
        "image_url": photo.get("image_src", {}).get("large", photo.get("image_url")),
        "pexels_url": photo.get("url")
    }


def format_product(product):
    return {
        "name": product.get("name"),
        "category": product.get("category"),
        "price": product.get("price", ""),
        "average_rating": product.get("average_rating", 0),
        "tags": product.get("tags", "").split("âº"),
        "image_url": product.get("images", [None])[0],
        "description": product.get("full_description", ""),
        "brand": product.get("manufacturer", ""),
        "store_url": product.get("brand_url", "")
    }

def trigger_background_personalization(user):
    user_text = embed_user(user)
    product_ids = query_faiss_index(user_text)
    update_document(
        collections.USERS,
        {"username": user["username"]},
        {"$set": {"personalized_product_ids": product_ids}}
    )


@router.get("/stream")
def get_stream(
    background_tasks: BackgroundTasks,
    user=Depends(get_current_user),
    page: int = Query(1, gt=0),
    page_size: int = 30
):
    update_document(
        "users",
        {"username": user["username"]},
        {"$set": {"last_active": datetime.utcnow()}}
    )

    photo_skip = (page - 1) * page_size
    photo_cursor = fetch_documents("photos").skip(photo_skip).limit(page_size)
    all_photos = [format_photo(p) for p in photo_cursor]
    photo_count = len(all_photos)

    product_ids = user.get("personalized_product_ids", [])
    if not product_ids:
        fallback_cursor = db["products"].aggregate([{"$sample": {"size": 100}}])
        fallback_ids = [str(p["_id"]) for p in fallback_cursor]
        background_tasks.add_task(trigger_background_personalization, user)
        product_ids = fallback_ids
    else:
        print(f"Personalized product IDs loaded: {len(product_ids)}")

    personalized_cursor = fetch_documents(
        "products",
        {"_id": {"$in": [ObjectId(pid) for pid in product_ids if ObjectId.is_valid(pid)]}}
    )
    personalized_products = [format_product(p) for p in personalized_cursor]

    explore_cursor = fetch_documents("products")
    explore_pool = [p for p in explore_cursor if str(p["_id"]) not in product_ids]
    shuffle(explore_pool)
    explore_products = [format_product(p) for p in explore_pool[:50]]

    # stream logic
    stream = []
    p_idx = e_idx = 0
    last_insert = None
    personalized_positions = set(range(9, photo_count, 10))
    explore_positions = set(i for i in range(6, photo_count, 7) if i not in personalized_positions)

    for i, photo in enumerate(all_photos):
        stream.append({"type": "photo", "data": photo})
        if i in personalized_positions and p_idx < len(personalized_products):
            stream.append({"type": "product", "data": personalized_products[p_idx]})
            p_idx += 1
            last_insert = "personalized"
        elif i in explore_positions and e_idx < len(explore_products):
            if last_insert != "explore":
                stream.append({"type": "product", "data": explore_products[e_idx]})
                e_idx += 1
                last_insert = "explore"
        else:
            last_insert = None

    return {"stream": stream, "page": page}
