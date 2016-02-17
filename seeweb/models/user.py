from datetime import datetime
import hashlib
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from seeweb.avatar import generate_default_user_avatar

from .described import Described
from .installed import Installed
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

    @staticmethod
    def create(session, uid, name, email):
        """Create a new user.

        Also create default avatar for this user.

        Args:
            session: (DBSession)
            uid: (str) user id
            name: (str) display name
            email: (str) email address

        Returns:
            (User)
        """
        user = User(id=uid, name=name, email=email)
        session.add(user)

        # create avatar
        generate_default_user_avatar(user)

        return user

    @staticmethod
    def remove(session, user):
        """Remove a user from database.

        Also remove user's avatar.

        Raises: UserWarning if user still own projects

        Args:
            session: (DBSession)
            user: (User)

        Returns:
            (True)
        """
        del session
        del user

        # remove avatar
        # TODO

        return True

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

    def install_project(self, session, project):
        """Install project in user installed projects

        Warnings: Does not test if user has permission to do that.

        Args:
            session: (DBSession)
            project: (Project)

        Returns:
            None
        """
        installed = Installed(user=self.id,
                              project=project.id,
                              date=datetime.now(),
                              version="0.0.0")
        session.add(installed)

    def uninstall_project(self, session, project):
        """Uninstall project from user installed projects

        Raises: UserWarning if project is not installed

        Args:
            session: (DBSession)
            project: (Project)

        Returns:
            None
        """
        for installed in self.installed:
            if installed.project == project.id:
                session.delete(installed)
                return

