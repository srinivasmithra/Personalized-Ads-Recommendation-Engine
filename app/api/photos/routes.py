from fastapi import APIRouter, Query
from app.db.mongo_methods import fetch_documents
from app.db.collection_names import collections

router = APIRouter(prefix="/photos", tags=["photos"])


def format_photo(photo):
    return {
        "alt": photo.get("alt"),
        "category": photo.get("category"),
        "photographer": photo.get("photographer"),
        "image_url": photo.get("image_src", {}).get("large", photo.get("image_url")),
        "pexels_url": photo.get("url")
    }


@router.get("/")
def get_photos(page: int = Query(1, gt=0), page_size: int = 10):
    skip = (page - 1) * page_size
    cursor = fetch_documents(collections.PHOTOS)
    photos = [format_photo(p) for i, p in enumerate(cursor) if i >= skip and i < skip + page_size]
    return {"photos": photos, "page": page}
