from pydantic import BaseModel
from datetime import datetime


class Template(BaseModel):
    input_variables: list[str]
    output_parser: str | None
    template: str
    template_format: str

class PromptTemplateBase(BaseModel):
    prompt_name: str
    prompt_template: Template
    tags: list[str]
    last_used: datetime | None

class PromptTemplateCreate(PromptTemplateBase):
    pass

class PromptTemplate(PromptTemplateBase):
    id: int
    created_at: datetime
    
    versions: list[PromptTemplateBase] | None = None

    class Config:
        orm_mode = True