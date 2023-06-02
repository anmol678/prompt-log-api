from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.sqlite.db import Base


class Template(Base):
    __tablename__ = 'templates'
    
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    last_used = Column(DateTime, nullable=True)
    
    input_variables = Column(JSON)
    prompt = Column(String)
    format = Column(String)
    
    version = Column(Integer)
    parent_template_id = Column(Integer, ForeignKey('prompt_templates.id'))


class PromptTemplate(Base):
    __tablename__ = 'prompt_templates'

    id = Column(Integer, primary_key=True)

    title = Column(String)
    templates = relationship('Template', lazy='joined')

    tags = Column(JSON)
    
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship('Project', backref='prompt_templates', lazy='joined')
