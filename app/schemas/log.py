from pydantic import BaseModel
from datetime import datetime


class Log(BaseModel):
    id: int
    
    function_name: str
    prompt: list | dict
    kwargs: dict
    
    request_start_time: datetime
    request_end_time: datetime
    response: list | dict

    provider_type: str
    token_usage: dict
    cost: float

    # project_id: int | None = None
    tags: list[str]

    # metadata: dict[str, str | None]
    
    # prompt_id: str | None
    # prompt_input_variables: dict[str, str | None]
    # prompt_version_number: int | None

    # score: int | None
        
    class Config:
        orm_mode = True
    
