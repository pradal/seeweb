from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
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

    def __repr__(self):
        return "<Team(id='%s', public='%s')>" % (self.id, self.public)

    def add_auth(self, user, role):
        """Add a new user to the team
        """
        actor = Actor(user=user.id, role=role)
        self.auth.append(actor)

        user.teams.append(self)

    def access_role(self, uid):
        """Check the type of access granted to a user.

        args:
         - uid (str): id of user willing to access team

        return:
         - role (Role): type of access granted to user
        """
        # check team auth for this user
        for actor in self.auth:
            if actor.user == uid:
                return actor.role

        # project is public
        if self.public:
            return Role.read
        else:
            return Role.denied
