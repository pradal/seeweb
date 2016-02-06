import hashlib
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .described import Described
from .models import Base


class User(Base, Described):
    """Represent a registered user
    """
    __tablename__ = 'users'

    id = Column(String(255), unique=True, primary_key=True)

    name = Column(String(255), nullable=False)  # display name
    email = Column(String(255), nullable=False)

    projects = relationship("Project")  # projects owned by user
    teams = relationship("TActor")  # teams the user belongs to

    installed = relationship("Installed")
    # projects installed in user local environment

    def __repr__(self):
        return "<User(id='%s', name='%s', email='%s')>" % (self.id,
                                                           self.name,
                                                           self.email)

    def md5(self):
        return hashlib.md5(self.email.strip().lower()).hexdigest()
