from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from .models import Base
from .rated import Rated


class Comment(Base, Rated):
    """Comment written by a user and associated with a project
    """
    __tablename__ = 'comments'

    id = Column(Integer, autoincrement=True, primary_key=True)
    project = Column(String(255), ForeignKey("projects.id"), nullable=False)
    author = Column(String(255), ForeignKey("users.id"), nullable=False)
    creation = Column(DateTime, nullable=False)

    message = Column(Text, default="")
    score = Column(Integer, default=1)  # TODO list of vote objects to avoid multiple same voters

    def __repr__(self):
        return "<Comment(id='%s')>" % self.id
