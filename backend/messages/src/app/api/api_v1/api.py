from fastapi import APIRouter

from app.api.api_v1.endpoints import email

api_router = APIRouter()
api_router.include_router(email.router, prefix="/mail", tags=["email"])
