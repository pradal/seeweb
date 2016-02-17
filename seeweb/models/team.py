from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from .described import Described
from .models import Base, get_by_id


class Team(Base, Described):
    """Group of users used to manage auth at a coarser level
    """
    __tablename__ = 'teams'

    id = Column(String(255), unique=True, primary_key=True)

    auth = relationship("TActor")

    def __repr__(self):
        return "<Team(id='%s')>" % self.id

    @staticmethod
    def get(session, tid):
        """Fetch a given team in the database.

        Args:
            session: (DBSession)
            tid: (str) team id

        Returns:
            (Team) or None if no team with this id is found
        """
        return get_by_id(session, Team, tid)


    def get_actor(self, uid):
        """Retrieve actor associated with this uid.

        Args:
            uid: (str) id of user

        Returns:
            (TActor) or None if no user in auth list
        """
        for actor in self.auth:
            if actor.user == uid:
                return actor

        return None
