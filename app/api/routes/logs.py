from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import dependencies
from app.crud import crud_log
from app.models.log import Log
from app.models.request import Request, RequestResponse


router = APIRouter()

@router.post("/logs", response_model=RequestResponse)
def create_log(*, db: Session = Depends(dependencies.get_db), request_in: Request) -> RequestResponse:
    log = crud_log.create(db=db, obj_in=request_in)
    if not log:
        raise HTTPException(
            status_code=400,
            detail="Error while creating Log",
        )
    return RequestResponse(request_id=log.id)


@router.get("/logs", response_model=list[Log])
def get_logs(*, db: Session = Depends(dependencies.get_db)) -> list[Log]:
    logs = crud_log.get_multi(db=db)
    return logs


@router.get("/logs/{id}", response_model=Log)
def get_log(*, db: Session = Depends(dependencies.get_db), id: int) -> Log:
    log = crud_log.get(db=db, id=id)
    if not log:
        raise HTTPException(
            status_code=404,
            detail="Log not found",
        )
    return log
