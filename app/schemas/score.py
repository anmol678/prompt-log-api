from pydantic import BaseModel

class Score(BaseModel):
    request_id: str
    score: int