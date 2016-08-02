from base64 import b64encode
from sqlalchemy import Column, ForeignKey, LargeBinary, String

from seeweb.models.models import get_by_id
from seeweb.models.research_object import ResearchObject


class ROData(ResearchObject):
    """Research Object base class for all ROs that have a binary content
    """
    __tablename__ = 'ro_datas'

    id = Column(String(255), ForeignKey('ros.id'), primary_key=True)
    value = Column(LargeBinary(), default="")

    __mapper_args__ = {
        'polymorphic_identity': 'data',
    }

    def __repr__(self):
        return "<ROData(id='%s'')>" % self.id

    @staticmethod
    def get(session, uid):
        """Fetch a given RO in the database.

        Args:
            session: (DBSession)
            uid: (str) RO id

        Returns:
            (ResearchObject) or None if no RO with this id is found
        """
        return get_by_id(session, ROData, uid)

    def init(self, session, ro_def):
        """Initialize this RO with a set of attributes

        Args:
            session (DBSession):
            ro_def (dict): set of properties to initialize this RO

        Returns:
            None
        """
        loc_def = dict(ro_def)
        value = loc_def.pop('value', "")

        ResearchObject.init(self, session, loc_def)
        self.value = value

    def repr_json(self, full=False):
        """Create a json representation of this object

        Args:
            full (bool): if True, also add all properties stored in definition
                         default False

        Returns:
            dict
        """
        print "JSON\n" * 10, full
        d = ResearchObject.repr_json(self, full=full)

        if full:
            d['value'] = b64encode(self.value)

        return d
