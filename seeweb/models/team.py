from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship

from .actor import Actor
from .auth import Role
from .models import Base


team_auth = Table('team_auth',
                  Base.metadata,
                  Column('team_id', String(255),
                         ForeignKey('team.id'),
                         primary_key=True),
                  Column('actor_id', Integer,
                         ForeignKey('actor.id'),
                         primary_key=True),
                  )


class Team(Base):
    __tablename__ = 'team'

    id = Column("id", String(255), ForeignKey('userid.id'), primary_key=True)

    auth = relationship("Actor", secondary=team_auth)

    description = Column(Text, default="")

    def __repr__(self):
        return "<Team(id='%s')>" % self.id

    def get_actor(self, uid):
        """Retrieve actor associated with this uid.
        """
        for i, actor in enumerate(self.auth_user):
            if actor.user == uid:
                return i, actor

        return None, None

    def add_auth(self, role, user=None):
        """Add a new user to the team
        """
        actor = Actor(user=user.id, role=role)
        self.auth_user.append(actor)
        user.teams.append(self)

    def update_auth(self, user, new_role):
        """Update role of user in the team
        """
        i, actor = self.get_actor(user.id)

        if new_role == Role.denied:  # remove user from team
            try:
                user.teams.remove(self)
            except ValueError:
                pass  # user already removed???

            if actor is not None:
                del self.auth_user[i]
        else:
            actor.role = new_role
