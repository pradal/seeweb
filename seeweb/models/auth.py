from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from .models import Base


class Role(object):
    """Defines types of action a user can perform on a team and or project
    """
    denied = 0
    view = 1
    install = 2
    edit = 3

    @staticmethod
    def from_str(role_str):
        """Convert a string into a Role object

        Args:
            role_str: (str) String representation of a Role

        Returns:
            (Role)
        """
        if role_str == "edit":
            return Role.edit

        if role_str == "install":
            return Role.install

        if role_str == "view":
            return Role.view

        return Role.denied

    @staticmethod
    def to_str(role):
        """Convert a Role object into a string.

        Args:
            role: (Role)

        Returns:
            (str)
        """
        if role == Role.edit:
            return "edit"

        if role == Role.install:
            return "install"

        if role == Role.view:
            return "view"

        return "denied"


class ROPolicy(Base):
    """Authorization policy item for ROs.

    Store the type of action a given actor can do on a RO
    """
    __tablename__ = 'ro_policies'

    id = Column(Integer, autoincrement=True, primary_key=True)
    ro = Column(String(32), ForeignKey("ros.id"))
    actor = Column(String(255), ForeignKey("actors.id"))
    role = Column(Integer)

    def __repr__(self):
        tpl = "<ROPolicy(id='%s', ro='%s', actor='%s', role='%s')>"
        return tpl % (self.id, self.ro, self.actor,  self.role)


class TPolicy(Base):
    """Authorization policy item for teams.

    Store the type of action a given actor can do on a team
    """
    __tablename__ = 't_policies'

    id = Column(Integer, autoincrement=True, primary_key=True)
    team = Column(String(255), ForeignKey("teams.id"))
    actor = Column(String(255), ForeignKey("actors.id"))
    is_team = Column(Boolean, default=False)
    role = Column(Integer)

    def __repr__(self):
        tpl = "<TPolicy(id='%s', team='%s', actor='%s', role='%s')>"
        return tpl % (self.id, self.team, self.actor, self.role)


class Authorized(object):
    """Base class for models with a list of authorization policies
    """

    def get_policy(self, uid):
        """Retrieve policy associated with a given actor.

        Args:
            uid: (str) id of actor

        Returns:
            (Policy) or None if no actor in auth list
        """
        for pol in self.auth:
            if pol.actor == uid:
                return pol

        return None

    def remove_policy(self, session, uid):
        """Remove access granted to actor

        Args:
            session: (DBSession)
            uid: (str) id of actor

        Returns:
            None
        """
        pol = self.get_policy(uid)
        if pol is not None:
            session.delete(pol)

    def update_policy(self, session, uid, new_role):
        """Update role of actor.

        Args:
            session: (DBSession)
            uid: (str) user id
            new_role: (Role)

        Returns:
            None
        """
        del session
        pol = self.get_policy(uid)
        pol.role = new_role
