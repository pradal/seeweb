from sqlalchemy import Boolean, Column, ForeignKey, String, Table
from sqlalchemy.orm import relationship
from models import Base


user_to_teams = Table('asso_user_teams',
                      Base.metadata,
                      Column('user_id', String(255),
                             ForeignKey('userid.id'),
                             primary_key=True),
                      Column('team_id', String(255),
                             ForeignKey('team.id'),
                             primary_key=True),
                      )


class UserId(Base):
    __tablename__ = 'userid'

    id = Column(String(255), unique=True, primary_key=True)
    is_team = Column(Boolean, default=False)
    teams = relationship("Team", secondary=user_to_teams)

    def __repr__(self):
        return "<UserId(id='%s')>" % self.id

    def is_member(self, tid):
        """Check if user is a direct member of the given team
        """
        for team in self.teams:
            if team.id == tid:
                return True

        return False
