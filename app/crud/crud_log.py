from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.request import Request
from app.sqlite.schemas.log import Log
from app.models.log import Log as LogPy, LogWithPromptVersion
from app.utils.cost import CostCalculator
from app.crud import crud_project, crud_prompt_template_log
from app.models.exceptions import DatabaseError


def create(db: Session, request: Request) -> Log:
    db_log = Log(
        function_name=request.function_name,
        prompt=request.function_args,
        kwargs=request.function_kwargs,
        
        request_start_time=request.request_start_time,
        request_end_time=request.request_end_time,
        response=request.request_response,
        
        provider_type=request.provider_type,
        token_usage=request.request_usage,
        cost=CostCalculator().calculate_cost(usage=request.request_usage, kwargs=request.function_kwargs),
        
        tags=request.tags,
        project_id=(
            crud_project.get_or_create(db, title=request.metadata['project']).id 
            if request.metadata and 'project' in request.metadata and request.metadata['project'] else None
        )
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    if db_log is None:
        raise DatabaseError("Error while logging request")
    return db_log

def get(db: Session, id: int) -> Log:
    db_log = (
        db.query(Log)
        .filter(Log.id == id)
        .first()
    )
    if db_log is None:
        raise DatabaseError("Request Log not found", 404)
    return db_log

def get_multi(db: Session, skip: int = 0, limit: int = 100) -> list[Log]:
    return (
        db.query(Log)
        .order_by(desc(Log.request_start_time))
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_multi_by_id(db: Session, ids: list[int]) -> list[Log]:
    return (
        db.query(Log)
        .filter(Log.id.in_(ids))
        .all()
    )

def get_for_prompt_template(db: Session, prompt_template_id: int) -> LogWithPromptVersion:
    pt_logs = crud_prompt_template_log.get_by_prompt_template(db, id=prompt_template_id)
    log_ids = [pt_log.log_id for pt_log in pt_logs]
    logs = get_multi_by_id(db, ids=log_ids)
    log_id_to_version = {pt_log.log_id: pt_log.version_number for pt_log in pt_logs}

    logs_with_versions = []
    for log in logs:
        log_dict = LogPy.from_orm(log).dict()
        log_dict['version_number'] = log_id_to_version[log.id]
        logs_with_versions.append(log_dict)
    return logs_with_versions

def update(db: Session, id: int, log: Log) -> Log:
    db_log = get(db, id=id)
    for key, value in log.dict().items():
        setattr(db_log, key, value)
    db.commit()
    db.refresh(db_log)
    return db_log

def delete(db: Session, id: int):
    db_log = get(db, id=id)
    db.delete(db_log)
    db.commit()
