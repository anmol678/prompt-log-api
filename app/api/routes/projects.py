from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import dependencies
from app.models.project import Project, ProjectCreate
from app.crud import crud_project
from app.models.exceptions import DatabaseError


router = APIRouter()


@router.post("/projects", response_model=Project)
def create_project(*, db: Session = Depends(dependencies.get_db), project_in: ProjectCreate):
    try:
        project = crud_project.create(db, project=project_in)
    except DatabaseError as e:
        raise HTTPException(
            status_code=e.code,
            detail=str(e.message),
        )
    return project


@router.get("/projects", response_model=list[Project])
def get_projects(*, db: Session = Depends(dependencies.get_db)):
    projects = crud_project.get_multi(db)
    return projects


@router.get("/projects/{id}", response_model=Project)
def get_project(*, db: Session = Depends(dependencies.get_db), id: int):
    project = crud_project.get(db, id=id)
    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )
    return project


@router.put("/projects/{id}", response_model=Project)
async def update_project(*, db: Session = Depends(dependencies.get_db), id: int, project_in: ProjectCreate):
    project = crud_project.get(db, id=id)
    if not project:
        raise HTTPException(
            status_code=404, 
            detail="Project not found",
        )
    project = crud_project.update(db, db_obj=project, project=project_in)
    return project
