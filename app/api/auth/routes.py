from fastapi import APIRouter, HTTPException
from app.db.mongo_methods import insert_single_document, fetch_documents
from app.db.collection_names import collections
from app.api.auth.schemas import UserSignup, UserLogin
from app.api.auth.auth_utils import hash_password, verify_password, create_access_token


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup")
def signup(user: dict):
    if "," not in user["interests"] or "," not in user["search_history"]:
        raise HTTPException(status_code=400, detail="Interests and search history must be comma-separated.")

    existing = list(fetch_documents(collections.USERS, {"username": user["username"]}))
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    user["password"] = hash_password(user["password"])
    user["interests"] = [i.strip() for i in user["interests"].split(",")]
    user["search_history"] = [i.strip() for i in user["search_history"].split(",")]
    insert_single_document("users", user)
    return {"message": "Signup successful"}



@router.post("/login")
def login(credentials: UserLogin):
    user_cursor = fetch_documents(collections.USERS, {"username": credentials.username})
    user = next(user_cursor, None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not verify_password(credentials.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token({"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}
