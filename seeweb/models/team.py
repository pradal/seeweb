from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from .actor import TActor
from .auth import Role
from .models import Base


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
        for actor in self.auth:
            if actor.user == uid:
                return actor

        return None

    def add_auth(self, session, uid, role, is_team=False):
        """Add a new user to the team

        args:
         - uid (user_id or team_id): id of new 'user'
         - role (Role): type of role to grant
        """
        actor = TActor(team=self.id, user=uid, role=role)
        session.add(actor)
        actor.is_team = is_team

    def remove_auth(self, session, uid):
        """Remove user from the team
        args:
         - uid (user_id or team_id): id of 'user'
        """
        actor = self.get_actor(uid)
        if actor is not None:
            session.delete(actor)

    def update_auth(self, session, uid, new_role):
        """Update role of user in the team
        args:
         - uid (user_id or team_id): id of 'user'
         - new_role (Role): type of role to grant
        """
        actor = self.get_actor(uid)
        actor.role = new_role
        session.add(actor)
