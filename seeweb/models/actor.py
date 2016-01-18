from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from models import Base


class PActor(Base):
    __tablename__ = 'p_actors'

    id = Column(Integer, autoincrement=True, primary_key=True)
    project = Column(String(255), ForeignKey("projects.id"))
    user = Column(String(255), ForeignKey("users.id"))
    is_team = Column(Boolean, default=False)
    role = Column(Integer)

    def __repr__(self):
        tpl = "<PActor(id='%s', project='%s', user='%s', role='%s')>"
        return tpl % (self.id, self.project, self.user,  self.role)


class TActor(Base):
    __tablename__ = 't_actors'

    id = Column(Integer, autoincrement=True, primary_key=True)
    team = Column(String(255), ForeignKey("teams.id"))
    user = Column(String(255), ForeignKey("users.id"))
    is_team = Column(Boolean, default=False)
    role = Column(Integer)

    def __repr__(self):
        tpl = "<TActor(id='%s', team='%s', user='%s', role='%s')>"
        return tpl % (self.id, self.team, self.user, self.role)
