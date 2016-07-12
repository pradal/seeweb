from sqlalchemy import Column, ForeignKey, String

from seeweb.models.models import get_by_id
from seeweb.models.research_object import ResearchObject


class ROInterface(ResearchObject):
    """Research Object that contains interface definition for data types ROs
    """
    __tablename__ = 'ro_interfaces'

    id = Column(String(255), ForeignKey('ros.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'interface',
    }

    def __repr__(self):
        return "<ROInterface(id='%s', name='%s')>" % (self.id,
                                                      self.title)

    @staticmethod
    def get(session, uid):
        """Fetch a given RO in the database.

        Args:
            session: (DBSession)
            uid: (str) RO id

        Returns:
            (ResearchObject) or None if no RO with this id is found
        """
        return get_by_id(session, ROInterface, uid)

    def repr_json(self):
        """Create a json representation of this object

        Returns:
            dict
        """
        d = ResearchObject.repr_json(self)
        return d
