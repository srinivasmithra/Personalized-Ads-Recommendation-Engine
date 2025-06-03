from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.api.auth.auth_utils import SECRET_KEY, ALGORITHM
from app.db.mongo_methods import fetch_documents
from app.db.collection_names import collections

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=401, detail="can not validate credentials of user")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user_cursor = fetch_documents(collections.USERS, {"username": username})
    user = next(user_cursor, None)
    if not user:
        raise credentials_exception
    return user
