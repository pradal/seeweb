from sqlalchemy import Column, ForeignKey, Integer
from uuid import uuid1

from ...models import Base
from .content_item import ContentItem


class Notebook(Base, ContentItem):
    """Store the properties of a notebook.
    """
    __tablename__ = 'notebooks'

    cnt = Column(Integer, ForeignKey("pjt_contents.id"), nullable=False)

    def __repr__(self):
        return "<Notebook(id='%s')>" % self.id

    @staticmethod
    def create(session, project, name):
        """Create a new notebook description and associate it to a project.

        Args:
            session: (DBSession)
            project: (Project) an already existing project
            name: (str) name of the notebook

        Returns:
            (Notebook)
        """
        cnt = project.get_content(session)

        notebook = Notebook(id=uuid1().hex, cnt=cnt.id, name=name)
        session.add(notebook)

        return notebook
