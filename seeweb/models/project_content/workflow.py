from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ...models import Base


class Workflow(Base):
    """Store the properties of a workflow.
    """
    __tablename__ = 'workflows'

    id = Column(Integer, autoincrement=True, primary_key=True)
    cnt = Column(Integer, ForeignKey("pjt_contents.id"), nullable=False)
    name = Column(String(255), nullable=False)
    author = Column(String(255), default="")
    nodes = relationship("NodeItem")
    links = relationship("LinkItem")

    def __repr__(self):
        return "<Workflow(id='%s')>" % self.id


class NodeItem(Base):
    """Instance of a workflow node in a workflow.
    """
    __tablename__ = 'node_items'

    id = Column(Integer, autoincrement=True, primary_key=True)
    workflow = Column(Integer, ForeignKey("workflows.id"))
    # node = Column(Integer, ForeignKey("workflow_nodes.id"))  # Too soon?
    node = Column(String(255), default="")
    x = Column(Integer, default=0)
    y = Column(Integer, default=0)

    out_links = Column(Integer, ForeignKey("link_items"))
    in_links = Column(Integer, ForeignKey("link_items"))


class LinkItem(Base):
    """Instance of a link in a workflow.
    """
    __tablename__ = 'link_items'

    id = Column(Integer, autoincrement=True, primary_key=True)
    workflow = Column(Integer, ForeignKey("workflows.id"))
    source = Column(Integer, ForeignKey("node_items.id"))
    source_port = Column(String(255), default="")
    target = Column(Integer, ForeignKey("node_items.id"))
    target_port = Column(String(255), default="")
