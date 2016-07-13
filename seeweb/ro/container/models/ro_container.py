from sqlalchemy import Column, ForeignKey, String

from seeweb.models.models import get_by_id
from seeweb.models.research_object import ResearchObject
from seeweb.models.ro_link import ROLink


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

    def init(self, session, ro_def):
        """Initialize this RO with a set of attributes

        Args:
            session (DBSession):
            ro_def (dict): set of properties to initialize this RO

        Returns:
            None
        """
        # remove attributes locally stored
        loc_def = dict(ro_def)
        contents = loc_def.pop('contents', [])

        ResearchObject.init(self, session, loc_def)

        for ro in contents:
            ROLink.connect(session, self.id, ro.id, "contains")
