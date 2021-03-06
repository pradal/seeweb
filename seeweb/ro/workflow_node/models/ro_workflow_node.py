from itertools import chain
from sqlalchemy import Column, ForeignKey, String

from seeweb.models.models import get_by_id
from seeweb.models.research_object import ResearchObject
from seeweb.models.ro_link import ROLink


__all__ = ["ROWorkflowNode"]


class ROWorkflowNode(ResearchObject):
    """Research Object that contains node for workflows
    """
    __tablename__ = 'ro_workflow_nodes'

    id = Column(String(255), ForeignKey('ros.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'workflow_node',
    }

    def __repr__(self):
        return "<ROWorkflowNode(id='%s', name='%s')>" % (self.id,
                                                         self.name)

    @staticmethod
    def get(session, uid):
        """Fetch a given RO in the database.

        Args:
            session: (DBSession)
            uid: (str) RO id

        Returns:
            (ResearchObject) or None if no RO with this id is found
        """
        return get_by_id(session, ROWorkflowNode, uid)

    def init(self, session, ro_def):
        """Initialize this RO with a set of attributes

        Args:
            session (DBSession):
            ro_def (dict): set of properties to initialize this RO

        Returns:
            None
        """
        loc_def = dict(ro_def)
        # check attributes
        if 'inputs' not in loc_def:
            loc_def['inputs'] = []
        if 'outputs' not in loc_def:
            loc_def['outputs'] = []

        ResearchObject.init(self, session, loc_def)

        # link to interfaces used by this node
        ports = chain(loc_def['inputs'], loc_def['outputs'])
        uids = set(port_def['interface'] for port_def in ports)
        for uid in uids:
            ROLink.connect(session, self.id, uid, 'use')
