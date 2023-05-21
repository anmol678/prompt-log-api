from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import dependencies
from app.crud import crud_log
from app.schemas.log import Log


router = APIRouter()

@router.get("/logs", response_model=list[Log])
def get_logs(*, db: Session = Depends(dependencies.get_db)):
    logs = crud_log.get_logs(db=db)
    return logs


@router.get("/logs/{log_id}", response_model=Log)
def get_log(*, db: Session = Depends(dependencies.get_db), log_id: int) -> Log:
    log = crud_log.get(db=db, id=log_id)
    if not log:
        raise HTTPException(
            status_code=404,
            detail="Log not found",
        )
    return log
