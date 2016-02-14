from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from seeweb.models import Base
from seeweb.models.described import Described


class WorkflowNode(Base, Described):
    """Store the properties of node, elements of a workflow.
    """
    __tablename__ = 'workflow_nodes'

    id = Column(Integer, autoincrement=True, primary_key=True)
    cnt = Column(Integer, ForeignKey("pjt_contents.id"), nullable=False)
    name = Column(String(255), nullable=False)
    author = Column(String(255), default="")
    function = Column(String(255), default="")
    inputs = relationship("NodeInput")
    outputs = relationship("NodeOutput")

    def __repr__(self):
        return "<WorkflowNode(id='%s')>" % self.id


class NodeInput(Base, Described):
    """Inputs of a node.
    """
    __tablename__ = 'node_inputs'

    id = Column(Integer, autoincrement=True, primary_key=True)
    node = Column(Integer, ForeignKey("workflow_nodes.id"))
    name = Column(String(255), nullable=False)
    interface = Column(String(255), default="")
    value = Column(String(255), default="")


class NodeOutput(Base, Described):
    """Inputs of a node.
    """
    __tablename__ = 'node_outputs'

    id = Column(Integer, autoincrement=True, primary_key=True)
    node = Column(Integer, ForeignKey("workflow_nodes.id"))
    name = Column(String(255), nullable=False)
    interface = Column(String(255), default="")

