from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .auth import Role
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

    def has_member(self, session, uid):
        """Check whether the team has a given member.

        Also check sub teams recursively.

        Args:
            session: (DBSession)
            uid: (str) user id

        Returns:
            (Bool) True if user is appears in the team or one
            of the sub teams recursively and its role is not
            'denied'.
        """
        actors = list(self.auth)
        while len(actors) > 0:
            actor = actors.pop(0)
            if actor.user == uid:
                return actor.role != Role.denied

            if actor.is_team:
                actors.extend(Team.get(session, actor.user).auth)

        return False

    def access_role(self, session, uid):
        """Check the type of access granted to a user.

        Args:
            session: (DBSession)
            uid: id of user to test

        Returns:
            (Role) type of role given to this user
        """
        # check team auth for this user, supersede sub_team auth
        actor = self.get_actor(uid)
        if actor is not None:
            return actor.role

        # check team auth in subteams
        role = Role.view  # teams are public by default

        for actor in self.auth:
            if actor.is_team:
                team = Team.get(session, actor.user)
                if team.has_member(session, uid):
                    role = max(role, actor.role)
                    # useful in case user is member of multiple teams

        return role
