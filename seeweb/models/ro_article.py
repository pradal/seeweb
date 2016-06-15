from datetime import datetime
from sqlalchemy import Column, ForeignKey, String

from seeweb.avatar import generate_default_ro_avatar

from .research_object import ResearchObject


class ROArticle(ResearchObject):
    """Research Object that contains reference to an article
    """
    __tablename__ = 'ro_articles'

    id = Column(String(255), ForeignKey('ros.id'), primary_key=True)
    doi = Column(String(255), default="")

    __mapper_args__ = {
        'polymorphic_identity': 'article',
    }

    def __repr__(self):
        return "<ROArticle(id='%s', doi='%s')>" % (self.id,
                                                   self.doi)

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

        ro = ROArticle(id=uid,
                       creator=creator_id, created=created,
                       version=version,
                       title=title)
        session.add(ro)

        # create avatar
        generate_default_ro_avatar(ro)

        return ro
