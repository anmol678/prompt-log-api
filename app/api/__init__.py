from fastapi import APIRouter
from app.api.routes import logs, project, template

api_router = APIRouter()

api_router.include_router(logs.router, tags=["Logs"])
api_router.include_router(project.router, tags=["Project"])
api_router.include_router(template.router, tags=["Prompt Template"])

