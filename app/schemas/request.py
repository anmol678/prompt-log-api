from pydantic import BaseModel
from datetime import datetime

class Request(BaseModel):
    function_name: str
    function_args: list | dict
    function_kwargs: dict
    
    provider_type: str

    request_response: list | dict
    request_start_time: datetime
    request_end_time: datetime
    request_usage: dict
    
    tags: list[str] | None = None
    
    # prompt_id: str | None = None
    # prompt_input_variables: dict | None = None
    # prompt_version: int | None = None

class RequestResponse(BaseModel):
    request_id: int