from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import dependencies
from app.schemas.prompt_template import PromptTemplate, PromptTemplateMutate
from app.crud import crud_prompt_template

router = APIRouter()

@router.get("/prompt_template", response_model=list[PromptTemplate])
def read_prompt_templates(skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)):
    templates = crud_prompt_template.get_multi(db, skip=skip, limit=limit)
    return templates

@router.post("/prompt_template", response_model=PromptTemplate)
def create_prompt_template(*, db: Session = Depends(dependencies.get_db), template_in: PromptTemplateMutate):
    template = crud_prompt_template.create(db=db, prompt_template=template_in)
    return template

# @router.put("/prompt_template/{id}", response_model=PromptTemplate)
# async def update_prompt_template(*, db: Session = Depends(dependencies.get_db), id: int, template_in: PromptTemplateMutate):
#     template = crud_prompt_template.get(db=db, id=id)
#     if not template:
#         raise HTTPException(status_code=404, detail="Prompt template not found")
#     template = crud_prompt_template.update(db=db, db_obj=template, prompt_template=template_in)
#     return template
