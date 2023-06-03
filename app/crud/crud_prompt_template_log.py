from sqlalchemy.orm import Session
from app.sqlite.schemas.prompt_template_log import PromptTemplateLog
from app.models.prompt_template_log import PromptTemplateLogCreate
from app.crud import crud_log, crud_prompt_template
from app.models.exceptions import DatabaseError

def get_by_prompt_template(db: Session, id: int) -> list[PromptTemplateLog]:
    return (
        db.query(PromptTemplateLog)
        .filter(PromptTemplateLog.prompt_template_id == id)
        .all()
    )

def create(db: Session, log_id: int, prompt_template_id: int, version_number: int) -> PromptTemplateLog:
    db_ptl = PromptTemplateLog(
        log_id=log_id,
        prompt_template_id=prompt_template_id,
        version_number=version_number
    )
    db.add(db_ptl)
    db.commit()
    if db_ptl is None:
        raise DatabaseError("Error while creating PromptTemplateLog association")
    return db_ptl

def create_association(db: Session, log_id: int, data: PromptTemplateLogCreate) -> PromptTemplateLog:
    crud_log.get(db, id=log_id)
    crud_prompt_template.get(db, id=data.prompt_template_id)
    if data.version_number is None:
        version_number = crud_prompt_template.get_latest_template_version(db, id=data.prompt_template_id).version
    else:
        crud_prompt_template.get_template_version(db, id=data.prompt_template_id, version=data.version_number)
        version_number = data.version_number
    return create(db, 
                  log_id=log_id, 
                  prompt_template_id=data.prompt_template_id, 
                  version_number=version_number)