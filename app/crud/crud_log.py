from sqlalchemy.orm import Session
from app.schemas.request import Request
from app.sqlite.models.log import Log
from datetime import datetime

def create(db: Session, request: Request):
    db_log = request_to_log(request=request)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get(db: Session, log_id: int):
    return db.query(Log).filter(Log.id == log_id).first()

def get_logs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Log).offset(skip).limit(limit).all()

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

    # calulcate price, metadata, score

    # request_start_time = datetime.strptime(request.request_start_time, "%Y-%m-%d %H:%M:%S")
    # request_end_time = datetime.strptime(request.request_end_time, "%Y-%m-%d %H:%M:%S")

    log = Log(
        engine = request.function_kwargs['model'] if request.function_kwargs and 'model' in request.function_kwargs else request.function_kwargs['model_name'] if request.function_kwargs and 'model_name' in request.function_kwargs else None,
        function_name=request.function_name,
        function_args=request.function_args,
        function_kwargs=request.function_kwargs,
        request_response=request.request_response,
        request_start_time=request.request_start_time,
        request_end_time=request.request_end_time,
        tags=request.tags,
        # prompt_id=request.prompt_id,
        # prompt_input_variables=request.prompt_input_variables,
        # prompt_version_number=request.prompt_version,
        provider_type=request.provider_type,
        # price=price,
        max_tokens=None if not request.function_kwargs or 'max_tokens' not in request.function_kwargs else request.function_kwargs['max_tokens'],
        # score=score,
        temperature=None if not request.function_kwargs or 'temperature' not in request.function_kwargs else request.function_kwargs['temperature'],
        tokens=0 if not request.request_usage or 'total_tokens' not in request.request_usage else request.request_usage['total_tokens'],
    )
    return log
