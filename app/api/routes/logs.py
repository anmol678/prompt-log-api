from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import dependencies
from app.models.log import Log
from app.models.request import Request, RequestResponse
from app.crud import crud_log


router = APIRouter()

@router.post("/logs", response_model=RequestResponse)
def create_log(*, db: Session = Depends(dependencies.get_db), request_in: Request):
    log = crud_log.create(db=db, obj_in=request_in)
    if not log:
        raise HTTPException(
            status_code=400,
            detail="Error while creating Log",
        )
    return RequestResponse(request_id=log.id)


@router.get("/logs", response_model=list[Log])
def get_logs(*, db: Session = Depends(dependencies.get_db)):
    logs = crud_log.get_multi(db=db)
    return logs


@router.get("/logs/{id}", response_model=Log)
def get_log(*, db: Session = Depends(dependencies.get_db), id: int):
    log = crud_log.get(db=db, id=id)
    if not log:
        raise HTTPException(
            status_code=404,
            detail="Log not found",
        )
    return log
