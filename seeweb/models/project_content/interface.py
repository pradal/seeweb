from sqlalchemy import Column, ForeignKey, Integer
from uuid import uuid1

from seeweb.models.models import Base, get_by_id
from .content_item import ContentItem


class Interface(Base, ContentItem):
    """Store the properties of an interface definition.
    """
    __tablename__ = 'interfaces'

    cnt = Column(Integer, ForeignKey("pjt_contents.id"), nullable=False)

    def __repr__(self):
        return "<Interface(id='%s')>" % self.id

    @staticmethod
    def get(session, iid):
        """Fetch a given interface from the database.

        Args:
            session: (DBSession)
            iid: (int) interface id

        Returns:
            (Interface) or None if no comment with this id is found
        """
        return get_by_id(session, Interface, iid)

    @staticmethod
    def create(session, project, name):
        """Create a new interface description and associate it to a project.

        Args:
            session: (DBSession)
            project: (Project) an already existing project
            name: (str) name of the interface

        Returns:
            (Interface)
        """
        cnt = project.get_content(session)

        item = Interface(id=uuid1().hex, cnt=cnt.id, name=name)
        session.add(item)

        return item


