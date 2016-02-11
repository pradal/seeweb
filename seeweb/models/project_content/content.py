from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ...models import Base


class Content(Base):
    """Describe the potential content of a project
    in terms of objects recognized by the platform.
    """
    __tablename__ = 'pjt_contents'

    id = Column(String(255), ForeignKey("projects.id"), primary_key=True)
    notebooks = relationship("Notebook")

    def __repr__(self):
        return "<Content(id='%s')>" % self.id
