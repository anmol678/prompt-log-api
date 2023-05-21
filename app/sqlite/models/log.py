from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from app.sqlite.db import Base

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True)
    
    function_name = Column(String)
    function_args = Column(JSON)
    function_kwargs = Column(JSON)
    
    request_start_time = Column(DateTime)
    request_end_time = Column(DateTime)
    request_response = Column(JSON)

    tags = Column(JSON)

    engine = Column(String)
    provider_type = Column(String)
    # metadata = Column(JSON)
    # price = Column(Float)
    max_tokens = Column(Integer)
    # score = Column(Integer)
    temperature = Column(Float)
    tokens = Column(Integer)

    # prompt_id = Column(String)
    # prompt_input_variables = Column(JSON)
    # prompt_version_number = Column(Integer)
    
    
