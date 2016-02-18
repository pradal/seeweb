from sqlalchemy import Column, ForeignKey, Integer
from uuid import uuid1

from ...models import Base
from .content_item import ContentItem


class Executable(Base, ContentItem):
    """Store the properties of a console script.
    """
    __tablename__ = 'executables'

    cnt = Column(Integer, ForeignKey("pjt_contents.id"), nullable=False)

    def __repr__(self):
        return "<Executable(id='%s')>" % self.id

    @staticmethod
    def create(session, project, name):
        """Create a new executable description and associate it to a project.

        Args:
            session: (DBSession)
            project: (Project) an already existing project
            name: (str) name of the executable

        Returns:
            (Executable)
        """
        cnt = project.get_content(session)

        executable = Executable(id=uuid1().hex, cnt=cnt.id, name=name)
        session.add(executable)

        return executable
