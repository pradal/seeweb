from sqlalchemy import Column, ForeignKey, Integer

from ...models import Base
from .content_item import ContentItem


class Notebook(Base, ContentItem):
    """Store the properties of a notebook.
    """
    __tablename__ = 'notebooks'

    cnt = Column(Integer, ForeignKey("pjt_contents.id"), nullable=False)

    def __repr__(self):
        return "<Notebook(id='%s')>" % self.id
