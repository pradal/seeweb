from sqlalchemy import Column, ForeignKey, Integer

from ...models import Base
from .content_item import ContentItem


class Executable(Base, ContentItem):
    """Store the properties of a console script.
    """
    __tablename__ = 'executables'

    cnt = Column(Integer, ForeignKey("pjt_contents.id"), nullable=False)

    def __repr__(self):
        return "<Executable(id='%s')>" % self.id
