from sqlalchemy import Column, ForeignKey, Integer

from seeweb.models.models import Base, get_by_id
from .content_item import ContentItem


class Workflow(Base, ContentItem):
    """Store the properties of a workflow.
    """
    __tablename__ = 'workflows'

    cnt = Column(Integer, ForeignKey("pjt_contents.id"), nullable=False)

    def __repr__(self):
        return "<Workflow(id='%s')>" % self.id

    @staticmethod
    def get(session, wid):
        """Fetch a given workflow in the database.

        Args:
            session: (DBSession)
            wid: (str) workflow id

        Returns:
            (Workflow) or None if no workflow with this id is found
        """
        return get_by_id(session, Workflow, wid)

