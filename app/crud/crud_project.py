from sqlalchemy.orm import Session, joinedload
from app.sqlite.schemas.project import Project
from app.models.project import ProjectCreate
from app.models.exceptions import DatabaseError


def create(db: Session, project: ProjectCreate) -> Project:
    existing_project = get_by_title(db, project.title)
    if existing_project:
        raise DatabaseError("A project with this title already exists.")
    db_project = Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    if db_project is None:
        raise DatabaseError("Error while creating Project")
    return db_project

def get(db: Session, id: int) -> Project:
    return db.query(Project).filter(Project.id == id).first()

def get_by_title(db: Session, title: str) -> Project:
    return db.query(Project).filter(Project.title == title).first()

def get_multi(db: Session, skip: int = 0, limit: int = 100) -> list[Project]:
    return db.query(Project).offset(skip).limit(limit).all()

def get_or_create(db: Session, title: str) -> Project:
    project = get_by_title(db, title)
    if project:
        return project
    else:
        return create(db, project=ProjectCreate(title=title))

def update(db: Session, db_obj: Project, project: ProjectCreate) -> Project:
    for key, value in project.dict().items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, id: int):
    db_obj = get(db, id)
    db.delete(db_obj)
    db.commit()
    