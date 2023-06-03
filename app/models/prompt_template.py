from pydantic import BaseModel
from datetime import datetime
from app.models.project import Project


class TemplateBase(BaseModel):
    prompt: str
    input_variables: list[str]
    format: str

class TemplateCreate(TemplateBase):
    pass

class Template(TemplateBase):
    id: int
    version: int

    created_at: datetime
    last_used: datetime | None

    class Config:
        orm_mode = True


class PromptTemplateBase(BaseModel):
    title: str
    tags: list[str]

class PromptTemplateCreate(PromptTemplateBase):
    template: TemplateCreate
    project: str | None = None

class PromptTemplate(PromptTemplateBase):
    id: int

    templates: list[Template]
    project: Project | None
    
    class Config:
        orm_mode = True
        
class PromptTemplatePatch(BaseModel):
    title: str | None = None
    tags: list[str] | None = None
    template: TemplateCreate | None = None
    project: str | None = None
