from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship

from .actor import Actor
from .auth import Role
from .models import Base


team_auth = Table('team_auth',
                  Base.metadata,
                  Column('team_id', String(255),
                         ForeignKey('teams.id'),
                         primary_key=True),
                  Column('actor_id', Integer,
                         ForeignKey('actors.id'),
                         primary_key=True),
                  )


class Team(Base):
    __tablename__ = 'teams'

    id = Column(String(255), unique=True, primary_key=True)

    public = Column(Boolean)
    auth = relationship("Actor", secondary=team_auth)

    description = Column(Text, default="")

    def __repr__(self):
        return "<Team(id='%s', public='%s')>" % (self.id, self.public)

    def get_actor(self, uid):
        """Retrieve actor associated with this uid.
        """
        for i, actor in enumerate(self.auth):
            if actor.user == uid:
                return i, actor

        return None, None

    def add_auth(self, user, role):
        """Add a new user to the team
        """
        actor = Actor(user=user.id, role=role)
        self.auth.append(actor)

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
                del self.auth[i]
        else:
            actor.role = new_role

    def access_role(self, uid):
        """Check the type of access granted to a user.

        args:
         - uid (str): id of user willing to access team

        return:
         - role (Role): type of access granted to user
        """
        # check team auth for this user
        i, actor = self.get_actor(uid)
        if actor is not None:
            return actor.role

        # project is public
        if self.public:
            return Role.read
        else:
            return Role.denied
