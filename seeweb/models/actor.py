from sqlalchemy import Column, ForeignKey, Integer, String
from models import Base


class UActor(Base):
    __tablename__ = 'uactors'

    id = Column(Integer, autoincrement=True, primary_key=True)
    user = Column(String(255), ForeignKey("users.id"), nullable=False)
    role = Column(Integer)

    def __repr__(self):
        return "<User(id='%s', user='%s', role='%s')>" % (self.id,
                                                          self.user,
                                                          self.role)


class TActor(Base):
    __tablename__ = 'tactors'

    id = Column(Integer, autoincrement=True, primary_key=True)
    team = Column(String(255), ForeignKey("teams.id"), nullable=False)
    role = Column(Integer)

    def __repr__(self):
        return "<User(id='%s', team='%s', role='%s')>" % (self.id,
                                                          self.team,
                                                          self.role)
