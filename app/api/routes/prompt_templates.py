from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import dependencies
from app.models.prompt_template import PromptTemplate, PromptTemplateCreate, PromptTemplatePatch
from app.crud import crud_prompt_template
from app.models.exceptions import DatabaseError


router = APIRouter()


@router.post("/prompt-templates", response_model=PromptTemplate)
def create_prompt_template(*, db: Session = Depends(dependencies.get_db), prompt_template_in: PromptTemplateCreate):
    try:
        prompt_template = crud_prompt_template.create_with_template(db, prompt_template=prompt_template_in)
    except DatabaseError as e:
        raise HTTPException(
            status_code=e.code,
            detail=str(e.message),
        )
    return prompt_template


@router.get("/prompt-templates", response_model=list[PromptTemplate])
def get_prompt_templates(*, db: Session = Depends(dependencies.get_db)):
    prompt_templates = crud_prompt_template.get_multi(db)
    return prompt_templates


@router.get("/prompt-templates/{id}", response_model=PromptTemplate)
def get_prompt_template(*, db: Session = Depends(dependencies.get_db), id: int):
    try:
        prompt_template = crud_prompt_template.get(db, id=id)
    except DatabaseError as e:
        raise HTTPException(
            status_code=e.code,
            detail=str(e.message),
        )
    return prompt_template


@router.patch("/prompt-templates/{id}", response_model=PromptTemplate)
def update_prompt_template(*, db: Session = Depends(dependencies.get_db), id: int, prompt_template_in: PromptTemplatePatch):
    try:
        prompt_template = crud_prompt_template.update_with_template(db, id=id, prompt_template=prompt_template_in)
    except DatabaseError as e:
        raise HTTPException(
            status_code=404,
            detail="Prompt Template not found",
        )
    return prompt_template
