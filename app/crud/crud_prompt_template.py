from sqlalchemy.orm import Session
from app.sqlite.schemas.prompt_template import Template, PromptTemplate
from app.models.prompt_template import TemplateCreate, PromptTemplateCreate, PromptTemplatePatch, PromptTemplateWithVersion, PromptTemplate as PromptTemplatePy
from datetime import datetime
from app.crud import crud_project, crud_prompt_template_log
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
        project_id=(
            crud_project.get_or_create(db, title=prompt_template.project).id
            if prompt_template.project else None
        )
    )
    db.add(db_prompt_template)
    db.commit()
    db.refresh(db_prompt_template)
    if db_prompt_template is None:
        raise DatabaseError("Error while creating Prompt Template")
    return db_prompt_template

def create_with_template(db: Session, prompt_template: PromptTemplateCreate) -> PromptTemplate:
    db_prompt_template = create_prompt_template(db, prompt_template=prompt_template)
    create_template(db, 
                    template=prompt_template.template, 
                    parent_template_id=db_prompt_template.id)
    return db_prompt_template

def get(db: Session, id: int) -> PromptTemplate:
    db_prompt_template = (
        db.query(PromptTemplate)
        .filter(PromptTemplate.id == id)
        .first()
    )
    if db_prompt_template is None:
        raise DatabaseError("Prompt Template not found", 404)
    return db_prompt_template

def get_multi(db: Session, skip: int = 0, limit: int = 100) -> list[PromptTemplate]:
    return (
        db.query(PromptTemplate)
        .filter(PromptTemplate.deleted_at == None)
        .order_by(PromptTemplate.id.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_multi_by_id(db: Session, ids: list[int]) -> list[PromptTemplate]:
    return (
        db.query(PromptTemplate)
        .filter(PromptTemplate.id.in_(ids))
        .filter(PromptTemplate.deleted_at == None)
        .all()
    )

def get_template_version(db: Session, id: int, version: int) -> Template:
    db_template = (
        db.query(Template)
        .filter(
            Template.parent_template_id == id, 
            Template.version == version
        )
        .first()
    )
    if db_template is None:
        raise DatabaseError("Template version not found", 404)
    return db_template

def get_latest_template_version(db: Session, id: int) -> Template:
    return (
        db.query(Template)
        .filter(Template.parent_template_id == id)
        .order_by(Template.version.desc())
        .first()
    )

def get_for_log(db: Session, log_id: int) -> list[PromptTemplateWithVersion]:
    pt_logs = crud_prompt_template_log.get_by_log(db, id=log_id)
    prompt_template_ids = [pt_log.prompt_template_id for pt_log in pt_logs]
    prompt_templates = get_multi_by_id(db, ids=prompt_template_ids)
    prompt_template_id_to_version = {pt_log.prompt_template_id: pt_log.version_number for pt_log in pt_logs}

    prompt_templates_with_version = []
    for prompt_template in prompt_templates:
        prompt_template_dict = PromptTemplatePy.from_orm(prompt_template).dict()
        prompt_template_dict['version_number'] = prompt_template_id_to_version[prompt_template.id]
        prompt_templates_with_version.append(prompt_template_dict)
    return prompt_templates_with_version

def update_with_template(db: Session, id: int, prompt_template: PromptTemplatePatch) -> PromptTemplate:
    db_prompt_template = get(db, id=id)

    if prompt_template.title is not None:
        db_prompt_template.title = prompt_template.title

    if prompt_template.tags is not None:
        db_prompt_template.tags = prompt_template.tags

    if prompt_template.project is not None:
        db_prompt_template.project_id = crud_project.get_or_create(db, title=prompt_template.project).id
    else:
        db_prompt_template.project_id = None
    
    if prompt_template.template is not None:
        latest_template = db_prompt_template.templates[0]
        if latest_template.prompt != prompt_template.template.prompt or latest_template.input_variables != prompt_template.template.input_variables:
            create_template(db, 
                            template=prompt_template.template, 
                            parent_template_id=id, 
                            version=(len(db_prompt_template.templates)+1))

    db.commit()
    db.refresh(db_prompt_template)
    return db_prompt_template

def delete(db: Session, id: int):
    db_obj = get(db, id=id)
    db.delete(db_obj)
    db.commit()

def soft_delete(db: Session, id: int):
    db_prompt_template = get(db, id=id)
    db_prompt_template.deleted_at = datetime.utcnow()
    db.commit()
  