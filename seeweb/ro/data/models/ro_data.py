import json
from sqlalchemy import Column, ForeignKey, String, Text

from seeweb.models.models import get_by_id
from seeweb.models.research_object import ResearchObject

from seeweb.ro.interface.models.ro_interface import any_uid


class ROData(ResearchObject):
    """Research Object base class for all ROs that associate a value
    to a given type (or interface).
    """
    __tablename__ = 'ro_datas'

    id = Column(String(255), ForeignKey('ros.id'), primary_key=True)
    interface = Column(String(255), ForeignKey('ro_interfaces.id'))
    value = Column(Text(), default="null")

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
        interface = loc_def.pop('interface', any_uid)
        value = loc_def.pop('value', None)

        ResearchObject.init(self, session, loc_def)

        self.interface = interface
        self.value = json.dumps(value)

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
            d['interface'] = self.interface
            d['value'] = json.loads(self.value)

        return d
