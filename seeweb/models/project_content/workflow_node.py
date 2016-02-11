from sqlalchemy import Column, ForeignKey, Integer, String

from ...models import Base


class WorkflowNode(Base):
    """Store the properties of node, elements of a workflow.
    """
    __tablename__ = 'workflow_nodes'

    id = Column(Integer, autoincrement=True, primary_key=True)
    cnt = Column(Integer, ForeignKey("pjt_contents.id"), nullable=False)
    name = Column(String(255), nullable=False)

    def __repr__(self):
        return "<WorkflowNode(id='%s')>" % self.id
