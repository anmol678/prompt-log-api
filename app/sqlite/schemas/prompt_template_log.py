from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.sqlite.db import Base


class PromptTemplateLog(Base):
    __tablename__ = 'prompt_template_logs'
   
    prompt_template_id = Column(Integer, ForeignKey('prompt_templates.id'), primary_key=True)
    log_id = Column(Integer, ForeignKey('logs.id'), primary_key=True)
    version_number = Column(Integer)
    prompt_template = relationship('PromptTemplate', backref='prompt_template_logs')
    log = relationship('Log', backref='prompt_template_logs')
