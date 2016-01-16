from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship

from .actor import TActor, UActor
from .auth import Role
from .models import Base


team_auth_users = Table('team_auth_users',
                        Base.metadata,
                        Column('team_id', String(255),
                               ForeignKey('teams.id'),
                               primary_key=True),
                        Column('actor_id', Integer,
                               ForeignKey('uactors.id'),
                               primary_key=True),
                        )


team_auth_teams = Table('team_auth_teams',
                        Base.metadata,
                        Column('team_id', String(255),
                               ForeignKey('teams.id'),
                               primary_key=True),
                        Column('actor_id', Integer,
                               ForeignKey('tactors.id'),
                               primary_key=True),
                        )


class Team(Base):
    __tablename__ = 'teams'

    id = Column(String(255), unique=True, primary_key=True)

    auth_user = relationship("UActor", secondary=team_auth_users)
    auth_team = relationship("TActor", secondary=team_auth_teams)

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

    def add_auth(self, role, user=None, team=None):
        """Add a new user to the team
        """
        if user is not None:
            actor = UActor(user=user.id, role=role)
            self.auth_user.append(actor)
            user.teams.append(self)
        elif team is not None:
            actor = TActor(team=team.id, role=role)
            self.auth_team.append(actor)
        else:
            raise NotImplementedError()

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
