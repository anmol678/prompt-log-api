from sqlalchemy.orm import Session, joinedload
from app.sqlite.schemas.template import PromptTemplate
from app.models.template import PromptTemplateCreate


def create(db: Session, obj_in: PromptTemplateCreate) -> PromptTemplate:
    db_template = PromptTemplate(**obj_in.dict())
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template

def get(db: Session, id: int) -> PromptTemplate:
    return db.query(PromptTemplate).filter(PromptTemplate.id == id).first()

def get_multi(db: Session, skip: int = 0, limit: int = 100) -> list[PromptTemplate]:
    return db.query(PromptTemplate).offset(skip).limit(limit).all()

def update(db: Session, db_obj: PromptTemplate, obj_in: PromptTemplateCreate) -> PromptTemplate:
    for key, value in obj_in.dict().items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, id: int):
    db_obj = get(db, id)
    db.delete(db_obj)
    db.commit()
