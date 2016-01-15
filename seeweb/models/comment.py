from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from models import Base


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, autoincrement=True, primary_key=True)
    project = Column(String(255), ForeignKey("projects.id"), nullable=False)
    author = Column(String(255), ForeignKey("users.id"), nullable=False)
    creation = Column(DateTime, nullable=False)

    message = Column(Text, default="")
    rating = Column(Integer, default=0)

    def __repr__(self):
        return "<Comment(id='%s')>" % self.id
