import hashlib
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .described import Described
from .models import Base, get_by_id


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

    @staticmethod
    def get(session, uid):
        """Fetch a given user in the database.

        Args:
            session: (DBSession)
            uid: (str) user id

        Returns:
            (User) or None if no user with this id is found
        """
        return get_by_id(session, User, uid)

    def md5(self):
        return hashlib.md5(self.email.strip().lower()).hexdigest()

    def has_installed(self, session, project):
        """Check whether the project has already been installed for this user

        Args:
            session: (DBSession)
            user: (User)
            project: (Project)

        Returns:
            (bool): True if project already in user installed list
        """
        del session

        for installed in self.installed:
            if installed.project == project.id:
                return True

        return False
