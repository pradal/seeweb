from datetime import datetime
from sqlalchemy import Column, ForeignKey, String

from seeweb.avatar import generate_default_ro_avatar

from seeweb.models.models import get_by_id
from seeweb.models.research_object import ResearchObject


class ROWorkflowNode(ResearchObject):
    """Research Object that contains node for workflows
    """
    __tablename__ = 'ro_workflow_nodes'

    id = Column(String(255), ForeignKey('ros.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'workflow_node',
    }

    def __repr__(self):
        return "<ROInterface(id='%s', name='%s')>" % (self.id,
                                                      self.title)

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

        ro = ROWorkflowNode(id=uid,
                            creator=creator_id, created=created,
                            version=version,
                            title=title)
        session.add(ro)

        # create avatar
        generate_default_ro_avatar(ro)

        return ro
