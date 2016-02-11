from sqlalchemy import Column, ForeignKey, Integer, String

from ...models import Base


class Notebook(Base):
    """Store the properties of a notebook.
    """
    __tablename__ = 'notebooks'

    id = Column(Integer, autoincrement=True, primary_key=True)
    cnt = Column(Integer, ForeignKey("pjt_contents.id"), nullable=False)
    name = Column(String(255), nullable=False)

    def __repr__(self):
        return "<Notebook(id='%s')>" % self.id
