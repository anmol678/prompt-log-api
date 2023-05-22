from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import dependencies
from app.models.project import Project, ProjectCreate
from app.crud import crud_project


router = APIRouter()

@router.post("/project", response_model=Project)
def create_project(*, db: Session = Depends(dependencies.get_db), project_in: ProjectCreate):
    project = crud_project.create(db=db, obj_in=project_in)
    if not project:
        raise HTTPException(
            status_code=400,
            detail="Error while creating Project",
        )
    return project


@router.get("/project", response_model=list[Project])
def get_projects(*, db: Session = Depends(dependencies.get_db)):
    projects = crud_project.get_multi(db=db)
    return projects


@router.get("/project/{id}", response_model=Project)
def get_project(*, db: Session = Depends(dependencies.get_db), id: int):
    project = crud_project.get(db=db, id=id)
    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )
    return project


@router.put("/project/{id}", response_model=Project)
async def update_project(*, db: Session = Depends(dependencies.get_db), id: int, project_in: ProjectCreate):
    project = crud_project.get(db=db, id=id)
    if not project:
        raise HTTPException(
            status_code=404, 
            detail="Project not found",
        )
    project = crud_project.update(db=db, db_obj=project, obj_in=project_in)
    return project
