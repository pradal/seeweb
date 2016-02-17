from sqlalchemy import Column, ForeignKey, Integer

from seeweb.models.models import Base, get_by_id
from .content_item import ContentItem


class WorkflowNode(Base, ContentItem):
    """Store the properties of node, elements of a workflow.
    """
    __tablename__ = 'workflow_nodes'

    cnt = Column(Integer, ForeignKey("pjt_contents.id"), nullable=False)

    def __repr__(self):
        return "<WorkflowNode(id='%s')>" % self.id

    @staticmethod
    def get(session, nid):
        """Fetch a given workflow node in the database.

        Args:
            session: (DBSession)
            nid: (str) workflow node id

        Returns:
            (WorkflowNode) or None if no node with this id is found
        """
        return get_by_id(session, WorkflowNode, nid)


