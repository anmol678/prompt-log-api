from fastapi import APIRouter
from app.api.routes import logs, projects, prompt_templates

api_router = APIRouter()

api_router.include_router(logs.router, tags=["Logs"])
api_router.include_router(projects.router, tags=["Project"])
api_router.include_router(prompt_templates.router, tags=["Prompt Template"])
