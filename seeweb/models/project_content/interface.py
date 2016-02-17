from sqlalchemy import Column, ForeignKey, Integer

from ...models import Base
from .content_item import ContentItem


class Interface(Base, ContentItem):
    """Store the properties of an interface definition.
    """
    __tablename__ = 'interfaces'

    cnt = Column(Integer, ForeignKey("pjt_contents.id"), nullable=False)

    def __repr__(self):
        return "<Interface(id='%s')>" % self.id
