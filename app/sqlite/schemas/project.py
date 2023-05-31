from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship
from app.sqlite.db import Base


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    tags = Column(JSON)

    logs = relationship('Log', back_populates='project')
