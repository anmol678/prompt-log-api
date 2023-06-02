from sqlalchemy.orm import Session
from app.sqlite.schemas.prompt_template_log import PromptTemplateLog


def get_by_prompt_template(db: Session, id: int) -> list[PromptTemplateLog]:
    return (
        db.query(PromptTemplateLog)
        .filter(PromptTemplateLog.prompt_template_id == id)
        .all()
    )
