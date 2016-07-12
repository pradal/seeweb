from sqlalchemy import Column, ForeignKey, String

from seeweb.models.models import get_by_id
from seeweb.models.research_object import ResearchObject


class ROContainer(ResearchObject):
    """Research Object that contains other ROs
    """
    __tablename__ = 'ro_containers'

    id = Column(String(255), ForeignKey('ros.id'), primary_key=True)
    ctype = Column(String(50), default="project")

    __mapper_args__ = {
        'polymorphic_identity': 'container',
    }

    def __repr__(self):
        return "<ROContainer(id='%s', type='%s')>" % (self.id,
                                                      self.ctype)

    @staticmethod
    def get(session, uid):
        """Fetch a given RO in the database.

        Args:
            session: (DBSession)
            uid: (str) RO id

        Returns:
            (ResearchObject) or None if no RO with this id is found
        """
        return get_by_id(session, ROContainer, uid)
