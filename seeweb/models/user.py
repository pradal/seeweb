import hashlib
from sqlalchemy import Column, ForeignKey, String, Table, Text
from sqlalchemy.orm import relationship

from .models import Base


user_installed = Table('user_installed',
                       Base.metadata,
                       Column('user_id', String(255), ForeignKey('users.id'),
                              primary_key=True),
                       Column('pkg_id', String(255),
                              ForeignKey('projects.id'),
                              primary_key=True),
                       )


class User(Base):
    __tablename__ = 'users'

    id = Column(String(255), unique=True, primary_key=True)

    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)

    description = Column(Text, default="")

    projects = relationship("Project")
    teams = relationship("TActor")

    installed = relationship("Project", secondary=user_installed)

    def __repr__(self):
        return "<User(id='%s', name='%s', email='%s')>" % (self.id,
                                                           self.name,
                                                           self.email)

    def md5(self):
        return hashlib.md5(self.email.strip().lower()).hexdigest()
