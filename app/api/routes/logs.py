from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import dependencies
from app.models.log import Log, LogWithPromptVersion
from app.models.request import Request, RequestResponse
from app.crud import crud_log, crud_prompt_template_log
from app.models.exceptions import DatabaseError
from app.models.prompt_template_log import PromptTemplateLogCreate


router = APIRouter()


@router.post("/logs", response_model=RequestResponse, status_code=status.HTTP_201_CREATED)
def create_log(*, db: Session = Depends(dependencies.get_db), request_in: Request):
    try:
        log = crud_log.create(db, request=request_in)
    except DatabaseError as e:
        raise HTTPException(
            status_code=e.code,
            detail=e.message,
        )
    return RequestResponse(request_id=log.id)


@router.get("/logs", response_model=list[Log])
def get_logs(*, db: Session = Depends(dependencies.get_db)):
    try:
        logs = crud_log.get_multi_with_prompt_templates(db)
    except DatabaseError as e:
        raise HTTPException(
            status_code=e.code,
            detail=e.message,
        )
    return logs


@router.get("/logs/{id}", response_model=Log)
def get_log(*, db: Session = Depends(dependencies.get_db), id: int):
    try:
        log = crud_log.get(db, id=id)
    except DatabaseError as e:
        raise HTTPException(
            status_code=e.code,
            detail=e.message,
        )
    return log


@router.get("/logs/prompt-template/{prompt_template_id}", response_model=list[LogWithPromptVersion])
def get_logs_for_prompt_template(*, db: Session = Depends(dependencies.get_db), prompt_template_id: int):
    logs = crud_log.get_for_prompt_template(db, prompt_template_id=prompt_template_id)
    return logs


@router.post("/logs/{id}/track", status_code=status.HTTP_201_CREATED)
def create_log_prompt_template_association(*, db: Session= Depends(dependencies.get_db), id: int, track_data: PromptTemplateLogCreate):
    try:
        new_association = crud_prompt_template_log.create_association(db, log_id=id, data=track_data)
    except DatabaseError as e:
        raise HTTPException(
            status_code=e.code,
            detail=e.message
        )
    return new_association