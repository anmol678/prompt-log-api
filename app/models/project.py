from pydantic import BaseModel


class ProjectBase(BaseModel):
    title: str
    tags: list[str] = []

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int

    class Config:
        from_attributes = True
        