from pydantic import BaseModel
from datetime import datetime


class ProjectBase(BaseModel):
    name: str
    tags: list[str]

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int

    class Config:
        orm_mode = True

