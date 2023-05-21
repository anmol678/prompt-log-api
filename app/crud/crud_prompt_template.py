# from sqlalchemy.orm import Session
# from app.sqlite.models.prompt_template import PromptTemplate
# from app.schemas.prompt_template import PromptTemplateMutate, PromptTemplateBase

# def get_multi(db: Session, *, skip: int = 0, limit: int = 100):
#     return db.query(PromptTemplate).offset(skip).limit(limit).all()

# def create(db: Session, *, prompt_template: PromptTemplateMutate) -> PromptTemplate:
#     db_obj = PromptTemplate(**prompt_template.dict())
#     db.add(db_obj)
#     db.commit()
#     db.refresh(db_obj)
#     return db_obj

# def get(db: Session, id: int) -> PromptTemplate:
#     return db.query(PromptTemplate).filter(PromptTemplate.id == id).first()

# # def update(
# #     self, db: Session, *, db_obj: PromptTemplate, prompt_template: PromptTemplateMutate
# # ):
# #     obj_data = jsonable_encoder(db_obj)
# #     update_data = prompt_template.dict(skip_defaults=True)
# #     for field in obj_data:
# #         if field in update_data:
# #             setattr(db_obj, field, update_data[field])
# #     db.add(db_obj)
# #     db.commit()
# #     db.refresh(db_obj)
# #     return db_obj

# def promptORM_to_prompt(*, prompt_template: PromptTemplate) -> PromptTemplateBase:

#     log = Log(
#         engine=None if not request.function_kwargs or 'model' not in request.function_kwargs else request.function_kwargs['model'],
#         function_name=request.function_name,
#         function_args=request.function_args,
#         function_kwargs=request.function_kwargs,
#         request_response=request.request_response,
#         request_start_time=request.request_start_time,
#         request_end_time=request.request_end_time,
#         tags=request.tags,
#         # prompt_id=request.prompt_id,
#         # prompt_input_variables=request.prompt_input_variables,
#         # prompt_version_number=request.prompt_version,
#         provider_type=request.provider_type,
#         # price=price,
#         max_tokens=None if not request.function_kwargs or 'max_tokens' not in request.function_kwargs else request.function_kwargs['max_tokens'],
#         # score=score,
#         temperature=None if not request.function_kwargs or 'temperature' not in request.function_kwargs else request.function_kwargs['temperature'],
#         tokens=0 if not request.request_response or 'usage' not in request.request_response else request.request_response['usage']['total_tokens'],
#     )
#     return log
