from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from models import Base


project_auth = Table('project_auth',
                     Base.metadata,
                     Column('project_id', String(255),
                            ForeignKey('projects.name'),
                            primary_key=True),
                     Column('actor_id', Integer,
                            ForeignKey('actors.id'),
                            primary_key=True),
                     )


class Project(Base):
    __tablename__ = 'projects'

    name = Column(String(255), unique=True, primary_key=True)
    owner = Column(String(255), ForeignKey("users.username"), nullable=False)

    public = Column(Boolean)
    auth = relationship("Actor", secondary=project_auth)

    def __repr__(self):
        return "<Project(name='%s', owner='%s', public='%s')>" % (self.name,
                                                                  self.owner,
                                                                  self.public)
