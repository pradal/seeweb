from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .actor import PActor
from .fmt import format_ratings
from .models import Base


class Project(Base):
    __tablename__ = 'projects'

    id = Column(String(255), unique=True, primary_key=True)
    owner = Column(String(255), ForeignKey("users.id"))
    public = Column(Boolean)
    auth = relationship("PActor")

    description = Column(Text, default="")

    doc_url = Column(Text, default="")
    doc = Column(Text, default="")

    src_url = Column(Text, default="")

    # rating
    rating_value = Column(Integer, default=50)
    rating_doc = Column(Integer, default=50)
    rating_install = Column(Integer, default=50)
    rating_usage = Column(Integer, default=50)

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

    def remove_auth(self, session, uid):
        """Remove user from the project
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

    def format_ratings(self):
        return format_ratings(self)
