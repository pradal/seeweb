from sqlalchemy import Column, ForeignKey, Integer, String

from .models import Base


class Dependency(Base):
    """Explicit names and info for project's dependencies
    """
    __tablename__ = 'dependencies'

    id = Column(Integer, autoincrement=True, primary_key=True)
    project = Column(String(255), ForeignKey("projects.id"), nullable=False)
    name = Column(String(255), nullable=False)
    version = Column(String(255), nullable=False)

    def __repr__(self):
        return "<Dependency(id='%s')>" % self.id
