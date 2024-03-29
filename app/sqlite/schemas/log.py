from sqlalchemy import Column, Integer, String, DateTime, JSON, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.sqlite.db import Base


class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    
    function_name = Column(String)
    prompt = Column(JSON)
    kwargs = Column(JSON)
    
    request_start_time = Column(DateTime)
    request_end_time = Column(DateTime)
    response = Column(JSON)

    provider_type = Column(String)
    token_usage = Column(JSON)
    cost = Column(Float)

    tags = Column(JSON)

    project_id = Column(Integer, ForeignKey('projects.id'), nullable=True)
    project = relationship('Project', backref='logs', lazy='joined')

    # score = Column(Integer)
