from sqlalchemy import Column, ForeignKey, Integer

from ...models import Base
from .content_item import ContentItem


class Workflow(Base, ContentItem):
    """Store the properties of a workflow.
    """
    __tablename__ = 'workflows'

    cnt = Column(Integer, ForeignKey("pjt_contents.id"), nullable=False)

    def __repr__(self):
        return "<Workflow(id='%s')>" % self.id
