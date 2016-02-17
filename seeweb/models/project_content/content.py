from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from ...models import Base


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
