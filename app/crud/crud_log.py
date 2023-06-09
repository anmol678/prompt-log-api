from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.request import Request
from app.sqlite.schemas.log import Log
from app.sqlite.schemas.prompt_template import PromptTemplate
from app.sqlite.schemas.prompt_template_log import PromptTemplateLog
from app.models.log import Log as LogPy, LogWithPromptVersion
from app.models.prompt_template import PromptTemplateWithVersion
from app.utils.cost import CostCalculator
from app.crud import crud_project, crud_prompt_template_log
from app.models.exceptions import DatabaseError
from collections import defaultdict


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

def get_multi_with_prompt_templates(db: Session) -> list[LogPy]:
    log_entries = db.query(Log,
                    PromptTemplate,
                    PromptTemplateLog.version_number)\
              .outerjoin(PromptTemplateLog,
                    Log.id == PromptTemplateLog.log_id)\
              .outerjoin(PromptTemplate,
                    PromptTemplateLog.prompt_template_id == PromptTemplate.id)\
              .all()
    logs_with_pt = defaultdict(lambda: {"log": None, "prompt_templates": []})
    logs_without_pt = {}

    for log, prompt_template, version in log_entries:
        if prompt_template is not None:
            if logs_with_pt[log.id]["log"] is None:
                logs_with_pt[log.id]["log"] = log
            logs_with_pt[log.id]["prompt_templates"].append(
                PromptTemplateWithVersion(**prompt_template.__dict__, version_number=version)
            )
        else:
            if log.id not in logs_with_pt:
                logs_without_pt[log.id] = log

    result_logs = []
    for log_dict in logs_with_pt.values():
        log = log_dict["log"]
        result_logs.append(
            LogPy(
                id=log.id,
                function_name=log.function_name,
                prompt=log.prompt,
                kwargs=log.kwargs,
                request_start_time=log.request_start_time,
                request_end_time=log.request_end_time,
                response=log.response,
                provider_type=log.provider_type,
                token_usage=log.token_usage,
                cost=log.cost,
                tags=log.tags,
                project=log.project,
                prompt_templates=log_dict["prompt_templates"]
            )
        )

    for log in logs_without_pt.values():
        result_logs.append(
            LogPy(
                id=log.id,
                function_name=log.function_name,
                prompt=log.prompt,
                kwargs=log.kwargs,
                request_start_time=log.request_start_time,
                request_end_time=log.request_end_time,
                response=log.response,
                provider_type=log.provider_type,
                token_usage=log.token_usage,
                cost=log.cost,
                tags=log.tags,
                project=log.project,
                prompt_templates=[]
            )
        )
    
    result_logs.sort(key=lambda x: x.request_start_time, reverse=True)
    return result_logs

def get_with_prompt_templates(db: Session, id: int) -> LogPy:
    log_entries = db.query(Log,
                    PromptTemplate,
                    PromptTemplateLog.version_number)\
              .outerjoin(PromptTemplateLog,
                    Log.id == PromptTemplateLog.log_id)\
              .outerjoin(PromptTemplate,
                    PromptTemplateLog.prompt_template_id == PromptTemplate.id)\
              .filter(Log.id == id)\
              .all()

    prompt_templates = []
    log = None
    for log, prompt_template, version in log_entries:
        if prompt_template is not None:
            prompt_templates.append(
                PromptTemplateWithVersion(**prompt_template.__dict__, version_number=version)
            )

    if log is None:
        raise DatabaseError("Request Log not found", 404)

    return LogPy(
        id=log.id,
        function_name=log.function_name,
        prompt=log.prompt,
        kwargs=log.kwargs,
        request_start_time=log.request_start_time,
        request_end_time=log.request_end_time,
        response=log.response,
        provider_type=log.provider_type,
        token_usage=log.token_usage,
        cost=log.cost,
        tags=log.tags,
        project=log.project,
        prompt_templates=prompt_templates
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
