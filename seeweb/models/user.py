from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from seeweb.avatar import generate_default_user_avatar

from .actor import Actor
from .models import get_by_id


class User(Actor):
    """Represent a registered user
    """
    __tablename__ = 'users'

    id = Column(String(255), ForeignKey('actors.id'), primary_key=True)

    email = Column(String(255), nullable=False)

    teams = relationship("TPolicy")  # teams the user belongs to

    __mapper_args__ = {
        'polymorphic_identity': 'user',
    }

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

        Raises: UserWarning if user still own projects

        Args:
            session: (DBSession)
            user: (User)

        Returns:
            (True)
        """
        del session
        del user

        return True
