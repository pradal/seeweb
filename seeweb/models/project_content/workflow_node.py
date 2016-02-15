from sqlalchemy import Column, ForeignKey, Integer

from ...models import Base
from .content_item import ContentItem


class WorkflowNode(Base, ContentItem):
    """Store the properties of node, elements of a workflow.
    """
    __tablename__ = 'workflow_nodes'

    cnt = Column(Integer, ForeignKey("pjt_contents.id"), nullable=False)

    def __repr__(self):
        return "<WorkflowNode(id='%s')>" % self.id
