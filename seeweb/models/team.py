from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from seeweb.avatar import (generate_default_team_avatar,
                           remove_team_avatar)

from .actor import Actor
from .auth import Authorized, Role, TPolicy
from .models import get_by_id


class Team(Actor, Authorized):
    """Group of users used to manage auth at a coarser level
    """
    __tablename__ = 'teams'

    id = Column(String(255), ForeignKey('actors.id'), primary_key=True)

    auth = relationship("TPolicy")

    __mapper_args__ = {
        'polymorphic_identity': 'team',
    }

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

    @staticmethod
    def create(session, uid, name=None):
        """Create a new team.

        Also create default avatar for the team.

        Args:
            session: (DBSession)
            uid: (str) team id
            name: (str) display name, default None means name=tid

        Returns:
            (Team)
        """
        if name is None:
            name = uid

        team = Team(id=uid, name=name)
        session.add(team)

        # create avatar
        generate_default_team_avatar(team)

        return team

    @staticmethod
    def remove(session, team):
        """Remove a given team from the database.

        Also remove team's avatar.

        Args:
            session: (DBSession)
            team: (Team)

        Returns:
            (True)
        """
        # remove avatar
        remove_team_avatar(team)

        # remove authorizations
        for pol in team.auth:
            session.delete(pol)

        # remove team
        session.delete(team)

        return True

    def add_policy(self, session, actor, role):
        """Add a new authorization policy for this team

        Args:
            session: (DBSession)
            actor: (Actor)
            role: (Role) role to grant to user

        Returns:
            None
        """
        pol = TPolicy(team=self.id, actor=actor.id, role=role)
        pol.is_team = isinstance(actor, Team)
        session.add(pol)

    def has_member(self, session, uid):
        """Check whether the team has a given member.

        Also check sub teams recursively.

        Args:
            session: (DBSession)
            uid: (str) user id

        Returns:
            (Bool) True if user appears in the team or one
            of the sub teams recursively and its role is not
            'denied'.
        """
        policies = list(self.auth)
        while len(policies) > 0:
            pol = policies.pop(0)
            if pol.actor == uid:
                return pol.role != Role.denied

            if isinstance(pol.actor, Team):
                policies.extend(Team.get(session, pol.actor).auth)

        return False

    def access_role(self, session, uid):
        """Check the type of access granted to an actor.

        Args:
            session: (DBSession)
            uid: id of actor to test

        Returns:
            (Role) type of role given to this actor
        """
        # check team auth for this actor, supersede sub_team auth
        pol = self.get_policy(uid)
        if pol is not None:
            return pol.role

        # check team auth in subteams
        role = Role.view  # teams are public by default

        for pol in self.auth:
            if isinstance(pol.actor, Team):
                team = Team.get(session, pol.user)
                if team.has_member(session, uid):
                    role = max(role, pol.role)
                    # useful in case actor is member of multiple teams

        return role
