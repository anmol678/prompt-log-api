from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON
from app.sqlite.db import Base
from datetime import datetime


class PromptTemplate(Base):
    __tablename__ = "prompt_templates"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now())
    last_used = Column(DateTime, nullable=True)
    prompt_name = Column(String)
    prompt_template = Column(JSON)
    tags = Column(JSON)
    versions = Column(JSON, nullable=True)
