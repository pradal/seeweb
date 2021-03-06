import json
from sqlalchemy import Column, ForeignKey, String, Text

from seeweb.models.models import get_by_id
from seeweb.models.research_object import ResearchObject
from seeweb.models.ro_link import ROLink

__all__ = ["ROInterface"]


any_uid = u"87b0e17658cc11e6afb6d4bed973e64a"


class ROInterface(ResearchObject):
    """Research Object that contains interface definition for data types ROs
    """
    __tablename__ = 'ro_interfaces'

    id = Column(String(255), ForeignKey('ros.id'), primary_key=True)

    schema = Column(Text, default="{}")

    __mapper_args__ = {
        'polymorphic_identity': 'interface',
    }

    def __repr__(self):
        return "<ROInterface(id='%s', name='%s')>" % (self.id,
                                                      self.name)

    def ancestors(self):
        """Fetch ancestors of this interface

        Returns:
            (list of str): list of ancestors ids
        """
        return [link.source for link in self.in_links
                if link.type == 'is_ancestor_of']

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
        schema = loc_def.pop('schema', "{}")
        ancestors = loc_def.pop('ancestors', [])

        ResearchObject.init(self, session, loc_def)
        self.schema = schema
        for ancestor in ancestors:
            ROLink.connect(session, ancestor, self.id, 'is_ancestor_of')

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
            d['schema'] = json.loads(self.schema)
            d['ancestors'] = self.ancestors()

        return d
