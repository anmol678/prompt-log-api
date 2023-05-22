from sqlalchemy.orm import Session, joinedload
from app.sqlite.schemas.project import Project
from app.models.project import ProjectCreate


def create(db: Session, obj_in: ProjectCreate) -> Project:
    db_project = Project(**obj_in.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def get(db: Session, id: int) -> Project:
    return db.query(Project).filter(Project.id == id).first()

def get_multi(db: Session, skip: int = 0, limit: int = 100) -> list[Project]:
    return db.query(Project).offset(skip).limit(limit).all()

def update(db: Session, db_obj: Project, obj_in: ProjectCreate) -> Project:
    for key, value in obj_in.dict().items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, id: int):
    db_obj = get(db, id)
    db.delete(db_obj)
    db.commit()
