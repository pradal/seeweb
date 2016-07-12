from sqlalchemy import Column, ForeignKey, String

from seeweb.models.models import get_by_id
from seeweb.models.research_object import ResearchObject


class ROScene3d(ResearchObject):
    """Research Object to display 3D stuff
    """
    __tablename__ = 'ro_scene3d'

    id = Column(String(255), ForeignKey('ros.id'), primary_key=True)
    scene = Column(String(50), default="")

    __mapper_args__ = {
        'polymorphic_identity': 'scene3d',
    }

    def __repr__(self):
        return "<ROScene3d(id='%s')>" % (self.id,)

    @staticmethod
    def get(session, uid):
        """Fetch a given RO in the database.

        Args:
            session: (DBSession)
            uid: (str) RO id

        Returns:
            (ResearchObject) or None if no RO with this id is found
        """
        return get_by_id(session, ROScene3d, uid)
