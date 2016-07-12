from sqlalchemy import Column, ForeignKey, String

from seeweb.models.models import get_by_id
from seeweb.models.research_object import ResearchObject


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
    def get(session, uid):
        """Fetch a given RO in the database.

        Args:
            session: (DBSession)
            uid: (str) RO id

        Returns:
            (ResearchObject) or None if no RO with this id is found
        """
        return get_by_id(session, ROArticle, uid)
