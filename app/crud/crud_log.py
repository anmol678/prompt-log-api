from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from app.models.request import Request
from app.sqlite.schemas.log import Log
from datetime import datetime
from app.utils.cost import CostCalculator
from app.crud import crud_project, crud_prompt_template_log


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
    return db_log

def get(db: Session, id: int) -> Log:
    return (
        db.query(Log)
        .filter(Log.id == id)
        .first()
    )

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

def get_for_prompt_template(db: Session, prompt_template_id: int) -> list[Log]:
    pt_logs = crud_prompt_template_log.get_by_prompt_template(db, id=prompt_template_id)
    log_ids = [pt_log.log_id for pt_log in pt_logs]
    logs = get_multi_by_id(db, ids=log_ids)
    log_id_to_version = {pt_log.log_id: pt_log.version_number for pt_log in pt_logs}

    for log in logs:
        log_dict = log.dict()
        log_dict['version_number'] = log_id_to_version[log.id]
        logs.append(log_dict)

    return logs

def update(db: Session, db_obj: Log, obj_in: Log) -> Log:
    for key, value in obj_in.dict().items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, id: int):
    db_obj = get(db, id=id)
    db.delete(db_obj)
    db.commit()
