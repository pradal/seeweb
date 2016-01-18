from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship

from .actor import PActor
from .auth import Role
from .models import Base


class Project(Base):
    __tablename__ = 'projects'

    id = Column(String(255), unique=True, primary_key=True)
    owner = Column(String(255), ForeignKey("users.id"))

    description = Column(Text, default="")

    doc_url = Column(Text, default="")
    doc = Column(Text, default="")

    src_url = Column(Text, default="")

    public = Column(Boolean)
    auth = relationship("PActor")

    def __repr__(self):
        return "<Project(id='%s', owner='%s', public='%s')>" % (self.id,
                                                                self.owner,
                                                                self.public)

    def get_actor(self, uid):
        """Retrieve actor associated with this uid.
        """
        for actor in self.auth:
            if actor.user == uid:
                return actor

        return None

    def add_auth(self, session, uid, role, is_team=False):
        """Add a new user,role authorization to the project
        """
        actor = PActor(project=self.id, user=uid, role=role)
        session.add(actor)
        actor.is_team = is_team

    def update_auth(self, session, uid, new_role):
        """Update role of user in the team
        args:
         - uid (user_id or team_id): id of 'user'
         - new_role (Role): type of role to grant
        """
        actor = self.get_actor(uid)

        if new_role == Role.denied:  # remove user from team
            if actor is not None:
                session.delete(actor)
        else:
            actor.role = new_role
            session.add(actor)
