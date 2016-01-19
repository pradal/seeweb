from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from .fmt import format_ratings
from .models import Base


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, autoincrement=True, primary_key=True)
    project = Column(String(255), ForeignKey("projects.id"), nullable=False)
    author = Column(String(255), ForeignKey("users.id"), nullable=False)
    creation = Column(DateTime, nullable=False)

    message = Column(Text, default="")
    score = Column(Integer, default=1)

    # rating
    rating_value = Column(Integer, default=50)
    rating_doc = Column(Integer, default=50)
    rating_install = Column(Integer, default=50)
    rating_usage = Column(Integer, default=50)

    def __repr__(self):
        return "<Comment(id='%s')>" % self.id

    def format_ratings(self):
        return format_ratings(self)
