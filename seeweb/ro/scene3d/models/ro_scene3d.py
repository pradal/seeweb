from datetime import datetime
from sqlalchemy import Column, ForeignKey, String, Text

from seeweb.avatar import generate_default_ro_avatar

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

    @staticmethod
    def create(session, uid, creator_id, title):
        """Create a new RO.

        Also create default avatar for this RO.

        Args:
            session: (DBSession)
            uid: (str) unique id for RO
            creator_id: (str) id of actor creating the object
            title: (str) name of this RO

        Returns:
            (ResearchObject)
        """
        created = datetime.now()
        version = 0

        ro = ROScene3d(id=uid,
                       creator=creator_id, created=created,
                       version=version,
                       title=title)
        session.add(ro)

        # create avatar
        generate_default_ro_avatar(ro)

        return ro
