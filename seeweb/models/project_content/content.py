from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from seeweb.models.models import Base, get_by_id


item_types = ["executables",
              "notebooks",
              "interfaces",
              "workflow_nodes",
              "workflows"]


class Content(Base):
    """Describe the potential content of a project
    in terms of objects recognized by the platform.
    """
    __tablename__ = 'pjt_contents'

    id = Column(String(255), ForeignKey("projects.id"), primary_key=True)
    executables = relationship("Executable")
    interfaces = relationship("Interface")
    notebooks = relationship("Notebook")
    workflow_nodes = relationship("WorkflowNode")
    workflows = relationship("Workflow")

    def __repr__(self):
        return "<Content(id='%s')>" % self.id

    @staticmethod
    def get(session, pid):
        """Fetch the content of a given project in the database.

        Args:
            session: (DBSession)
            pid: (str) project id

        Returns:
            (Content) or None if no project with this id is found
        """
        return get_by_id(session, Content, pid)


