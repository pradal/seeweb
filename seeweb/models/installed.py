from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from .models import Base


class Installed(Base):
    """Information attached to installation of a project
    in a user workspace
    """
    __tablename__ = 'installed'

    id = Column(Integer, autoincrement=True, primary_key=True)
    user = Column(String(255), ForeignKey("users.id"), nullable=False)
    project = Column(String(255), ForeignKey("projects.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    version = Column(String(255), nullable=False)

    def __repr__(self):
        return "<Installed(id='%s')>" % self.id
