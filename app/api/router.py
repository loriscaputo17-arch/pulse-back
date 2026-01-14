from fastapi import APIRouter
from app.api import users, tracks, search

api_router = APIRouter()

api_router.include_router(users.router)
api_router.include_router(tracks.router)
api_router.include_router(search.router)
