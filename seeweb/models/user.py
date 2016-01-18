# import hashlib
from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from .auth import Role
from .models import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(String(255), unique=True, primary_key=True)

    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)

    description = Column(Text, default="")

    projects = relationship("Project")
    teams = relationship("TActor")

    def __repr__(self):
        return "<User(id='%s', name='%s', email='%s')>" % (self.id,
                                                           self.name,
                                                           self.email)

    # def md5(self):
    #     return hashlib.md5(self.email.strip().lower()).hexdigest()
