from pydantic import BaseModel
from datetime import datetime
from app.models.project import Project


class LogBase(BaseModel):
    function_name: str
    prompt: list | dict
    kwargs: dict
    
    request_start_time: datetime
    request_end_time: datetime
    response: list | dict

    provider_type: str
    token_usage: dict
    cost: float

    tags: list[str]
    project: Project | None = None

class LogWithPromptVersion(LogBase):
    id: int
    version_number: int

    class Config:
        orm_mode = True

class Log(LogBase):
    id: int

    class Config:
        orm_mode = True

    # score: int | None
    