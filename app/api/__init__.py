from fastapi import APIRouter
from app.api.routes import logs, project, prompt_template

api_router = APIRouter()

api_router.include_router(logs.router, tags=["Logs"])
api_router.include_router(project.router, tags=["Project"])
api_router.include_router(prompt_template.router, tags=["Prompt Template"])

