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

    @staticmethod
    def create(session, project, node_def):
        """Create a new node description and associate it to a project.

        Args:
            session: (DBSession)
            project: (Project) an already existing project
            node_def: (dict of node prop) node definition

        Returns:
            (WorkflowNode)
        """
        cnt = project.get_content(session)

        node = WorkflowNode(id=node_def['id'],
                            cnt=cnt.id,
                            name=node_def['name'])
        session.add(node)
        node.store_description(node_def['description'])
        node.store_definition(node_def)

        return node
