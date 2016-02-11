from sqlalchemy import Column, ForeignKey, Integer, String

from ...models import Base


class Workflow(Base):
    """Store the properties of a workflow.
    """
    __tablename__ = 'workflows'

    id = Column(Integer, autoincrement=True, primary_key=True)
    cnt = Column(Integer, ForeignKey("pjt_contents.id"), nullable=False)
    name = Column(String(255), nullable=False)

    def __repr__(self):
        return "<Workflow(id='%s')>" % self.id
