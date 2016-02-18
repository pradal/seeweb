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

    @staticmethod
    def create(session, project, workflow_def):
        """Create a new workflow description and associate it to a project.

        Args:
            session: (DBSession)
            project: (Project) an already existing project
            workflow_def: (dict of (str, any)) workflow definition

        Returns:
            (Workflow)
        """
        cnt = project.get_content(session)

        workflow = Workflow(id=workflow_def['id'],
                            cnt=cnt.id,
                            name=workflow_def['name'])
        session.add(workflow)
        workflow.store_description(workflow_def['description'])
        workflow.store_definition(workflow_def)

        return workflow

