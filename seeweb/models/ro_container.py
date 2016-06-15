from datetime import datetime
from sqlalchemy import Column, ForeignKey, String

from seeweb.avatar import generate_default_ro_avatar

from .research_object import ResearchObject


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
    def create(session, uid, creator_id, title):
        """Create a new RO.

        Also create default avatar for this user.

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

        ro = ROContainer(id=uid,
                         creator=creator_id, created=created,
                         version=version,
                         title=title)
        session.add(ro)

        # create avatar
        generate_default_ro_avatar(ro)

        return ro