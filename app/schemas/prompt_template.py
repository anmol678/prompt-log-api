from pydantic import BaseModel
from datetime import datetime

class Template(BaseModel):
    input_variables: list[str]
    output_parser: str | None
    template: str
    template_format: str

class PromptTemplateBase(BaseModel):
    created_at: datetime
    deleted: bool
    id: int
    last_used: datetime | None
    prompt_name: str
    prompt_template: Template
    tags: list[str]

class PromptTemplate(PromptTemplateBase):
    versions: list[PromptTemplateBase]

class PromptTemplateMutate(BaseModel):
    prompt_name: str
    prompt_template: Template
    tags: list[str]