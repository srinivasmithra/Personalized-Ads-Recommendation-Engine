from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth.routes import router as auth_router
from app.api.recommend.stream import router as stream_router
from app.api.photos.routes import router as photos_router

app = FastAPI()

# Allow all
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# all routers
app.include_router(auth_router)
app.include_router(stream_router)
app.include_router(photos_router)

