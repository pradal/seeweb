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

    def init(self, session, ro_def):
        """Initialize this RO with a set of attributes

        Args:
            session (DBSession):
            ro_def (dict): set of properties to initialize this RO

        Returns:
            None
        """
        loc_def = dict(ro_def)
        doi = loc_def.pop('doi', "")

        ResearchObject.init(self, session, loc_def)
        self.doi = doi

    def repr_json(self, full=False):
        """Create a json representation of this object

        Args:
            full (bool): if True, also add all properties stored in definition
                         default False

        Returns:
            dict
        """
        d = ResearchObject.repr_json(self, full=full)

        if full:
            d['doi'] = self.doi

        return d
