from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import dependencies
from app.models.template import PromptTemplate, PromptTemplateCreate
from app.crud import crud_template

router = APIRouter()

@router.post("/template", response_model=PromptTemplate)
def create_template(*, db: Session = Depends(dependencies.get_db), template_in: PromptTemplateCreate):
    template = crud_template.create(db=db, obj_in=template_in)
    if not template:
        raise HTTPException(
            status_code=400,
            detail="Error while creating Template",
        )
    return template


@router.get("/template", response_model=list[PromptTemplate])
def get_template(skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)):
    templates = crud_template.get_multi(db, skip=skip, limit=limit)
    return templates


@router.get("/template/{id}", response_model=PromptTemplate)
def get_templates(*, db: Session = Depends(dependencies.get_db), id: int) -> PromptTemplate:
    template = crud_template.get(db, id=id)
    if not template:
        raise HTTPException(
            status_code=404,
            detail="Template not found",
        )
    return template


@router.put("/template/{id}", response_model=PromptTemplate)
async def update_project(*, db: Session = Depends(dependencies.get_db), id: int, template_in: PromptTemplateCreate):
    template = crud_template.get(db=db, id=id)
    if not template:
        raise HTTPException(
            status_code=404, 
            detail="Project not found",
        )
    template = crud_template.update(db=db, db_obj=template, obj_in=template_in)
    return template
