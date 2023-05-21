from pydantic import BaseModel
from datetime import datetime

class Log(BaseModel):
    id: int
    
    function_args: dict[str, str | None]
    function_kwargs: dict[str, str | None]
    function_name: str
    
    engine: str
    provider_type: str
    max_tokens: int | None
    temperature: float
    tokens: int
    # metadata: dict[str, str | None]
    # price: float
    
    # prompt_id: str | None
    # prompt_input_variables: dict[str, str | None]
    # prompt_version_number: int | None
    
    request_end_time: datetime
    request_response: dict[str, str | None]
    request_start_time: datetime

    # score: int | None
    
    tags: list[str]
    
