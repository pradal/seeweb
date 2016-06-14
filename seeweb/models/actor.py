from sqlalchemy import Column, String

from .described import Described
from .models import Base, get_by_id


class Actor(Base, Described):
    """Base class for all actors (either users or teams)
    """

    __tablename__ = 'actors'

    id = Column(String(255), unique=True, primary_key=True)
    type = Column(String(50))

    name = Column(String(255), nullable=False)  # display name

    __mapper_args__ = {
        'polymorphic_identity': 'actor',
        'polymorphic_on': type
    }

    def __repr__(self):
        return "<Actor(id='%s', name='%s'>" % (self.id,
                                               self.name)

    @staticmethod
    def get(session, uid):
        """Fetch a given actor in the database.

        Args:
            session: (DBSession)
            uid: (str) actor id

        Returns:
            (Actor) or None if no actor with this id is found
        """
        return get_by_id(session, Actor, uid)
