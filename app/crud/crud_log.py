from sqlalchemy.orm import Session, joinedload
from app.models.request import Request
from app.sqlite.schemas.log import Log
from datetime import datetime
from app.utils.cost import CostCalculator


def create(db: Session, request: Request):
    db_log = request_to_log(request=request)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get(db: Session, log_id: int):
    return db.query(Log).options(joinedload(Log.project)).filter(Log.id == log_id).first()

def get_logs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Log).options(joinedload(Log.project)).offset(skip).limit(limit).all()

def update(db: Session, log: Log):
    db_log = get(db, log.id)
    for key, value in log.dict().items():
        setattr(db_log, key, value)
    db.commit()
    db.refresh(db_log)
    return db_log

def delete(db: Session, log_id: int):
    db_log = get(db, log_id)
    db.delete(db_log)
    db.commit()

def request_to_log(*, request: Request):

    # project, metadata, score, prompt_template

    # request_start_time = datetime.strptime(request.request_start_time, "%Y-%m-%d %H:%M:%S")
    # request_end_time = datetime.strptime(request.request_end_time, "%Y-%m-%d %H:%M:%S")

    log = Log(
        function_name=request.function_name,
        prompt=request.function_args,
        kwargs=request.function_kwargs,
        
        request_start_time=request.request_start_time,
        request_end_time=request.request_end_time,
        response=request.request_response,
        
        provider_type=request.provider_type,
        token_usage=request.request_usage,
        cost=CostCalculator().calculate_cost(usage=request.request_usage, kwargs=request.function_kwargs),
        project_id=request.project_id,
        tags=request.tags,

        # prompt_id=request.prompt_id,
        # prompt_input_variables=request.prompt_input_variables,
        # prompt_version_number=request.prompt_version,
    )
    return log
