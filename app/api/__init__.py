from fastapi import APIRouter
from app.api.routes import request, prompt_template, logs

api_router = APIRouter()

api_router.include_router(request.router, tags=["Request"])
api_router.include_router(prompt_template.router, tags=["Prompt Template"])
api_router.include_router(logs.router, tags=["Logs"])
