from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.sqlite.schemas.prompt_template import Template, PromptTemplate
from app.models.prompt_template import TemplateCreate, PromptTemplateCreate, PromptTemplatePatch
from datetime import datetime
from app.crud import crud_project
from app.models.exceptions import DatabaseError


def create_template(db: Session, template: TemplateCreate, parent_template_id: int) -> Template:
    db_template = Template(
        prompt=template.prompt,
        input_variables=template.input_variables,
        format=template.format,
        version=1,
        parent_template_id=parent_template_id,
        created_at=datetime.utcnow(),
        last_used=None
    )
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    if db_template is None:
        raise DatabaseError("Error while creating Template")
    return db_template

def create_prompt_template(db: Session, prompt_template: PromptTemplateCreate) -> PromptTemplate:
    db_prompt_template = PromptTemplate(
        title=prompt_template.title,
        tags=prompt_template.tags,
        project_id=crud_project.get_or_create(db, title=prompt_template.project).id
    )
    db.add(db_prompt_template)
    db.commit()
    db.refresh(db_prompt_template)
    if db_prompt_template is None:
        raise DatabaseError("Error while creating Prompt Template")
    return db_prompt_template

def create_with_template(db: Session, prompt_template: PromptTemplateCreate) -> PromptTemplate:
    db_prompt_template = create_prompt_template(db, prompt_template=prompt_template)
    create_template(db, template=prompt_template.template, parent_template_id=db_prompt_template.id)
    return db_prompt_template

def get(db: Session, id: int) -> PromptTemplate:
    return (
        db.query(PromptTemplate)
        .filter(PromptTemplate.id == id)
        .first()
    )

def get_multi(db: Session, skip: int = 0, limit: int = 100) -> list[PromptTemplate]:
    return (
        db.query(PromptTemplate)
        .order_by(desc(PromptTemplate.created_at))
        .offset(skip)
        .limit(limit)
        .all()
    )

    