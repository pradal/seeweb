from sqlalchemy import Column, ForeignKey, Integer

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


