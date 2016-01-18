from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from .actor import TActor
from .auth import Role
from .models import Base, DBSession


class Team(Base):
    __tablename__ = 'teams'

    id = Column(String(255), unique=True, primary_key=True)

    description = Column(Text, default="")

    auth = relationship("TActor")

    def __repr__(self):
        return "<Team(id='%s')>" % self.id

    def get_actor(self, uid):
        """Retrieve actor associated with this uid.
        """
        for i, actor in enumerate(self.auth):
            if actor.user == uid:
                return i, actor

        return None, None

    def add_auth(self, uid, role, is_team=False):
        """Add a new user to the team

        args:
         - uid (user_id or team_id): id of new 'user'
         - role (Role): type of role to grant
        """
        session = DBSession()
        actor = TActor(team=self.id, user=uid, role=role)
        actor.is_team = is_team
        session.add(actor)
        # self.auth_user.append(actor)
        # user.teams.append(self)

    def update_auth(self, uid, new_role):
        """Update role of user in the team
        args:
         - uid (user_id or team_id): id of 'user'
         - new_role (Role): type of role to grant
        """
        i, actor = self.get_actor(uid)

        if new_role == Role.denied:  # remove user from team
            # try:
            #     user.teams.remove(self)
            # except ValueError:
            #     pass  # user already removed???
            session = DBSession()
            if actor is not None:
                session.delete(actor)
        else:
            actor.role = new_role
