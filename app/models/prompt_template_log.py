from pydantic import BaseModel
from app.models.prompt_template import PromptTemplate


class PromptTemplateLog(BaseModel):
    log_id: int
    prompt_template: PromptTemplate
    version_number: int
    
    class Config:
        from_attributes = True

class PromptTemplateLogCreate(BaseModel):
    prompt_template_id: int
    version_number: int | None
