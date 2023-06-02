from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.sqlite.schemas.prompt_template import Template, PromptTemplate
from app.models.prompt_template import TemplateCreate, PromptTemplateCreate, PromptTemplatePatch
from datetime import datetime
from app.crud import crud_project
from app.models.exceptions import DatabaseError


def create_template(db: Session, template: TemplateCreate, parent_template_id: int, version: int = 1) -> Template:
    db_template = Template(
        prompt=template.prompt,
        input_variables=template.input_variables,
        format=template.format,
        version=version,
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
        .offset(skip)
        .limit(limit)
        .all()
    )

def update_with_template(db: Session, id: int, prompt_template: PromptTemplatePatch) -> PromptTemplate:
    db_prompt_template = get(db, id=id)

    if db_prompt_template is None:
        raise DatabaseError("Prompt Template not found")

    if prompt_template.title is not None:
        db_prompt_template.title = prompt_template.title

    if prompt_template.tags is not None:
        db_prompt_template.tags = prompt_template.tags

    if prompt_template.project is not None:
        db_prompt_template.project_id = crud_project.get_or_create(db, title=prompt_template.project).id
    
    if prompt_template.template is not None:
        create_template(db, template=prompt_template.template, parent_template_id=id, version=(len(db_prompt_template.templates)+1))

    db.commit()
    db.refresh(db_prompt_template)
    return db_prompt_template

def delete(db: Session, id: int):
    db_obj = get(db, id=id)
    db.delete(db_obj)
    db.commit()
  