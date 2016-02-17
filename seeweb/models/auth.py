
class Role(object):
    """Defines types of action a user can perform on a team and or project
    """
    denied = 0
    view = 1
    install = 2
    edit = 3

    @staticmethod
    def from_str(role_str):
        """Convert a string into a Role object

        Args:
            role_str: (str) String representation of a Role

        Returns:
            (Role)
        """
        if role_str == "edit":
            return Role.edit

        if role_str == "install":
            return Role.install

        if role_str == "view":
            return Role.view

        return Role.denied

    @staticmethod
    def to_str(role):
        """Convert a Role object into a string.

        Args:
            role: (Role)

        Returns:
            (str)
        """
        if role == Role.edit:
            return "edit"

        if role == Role.install:
            return "install"

        if role == Role.view:
            return "view"

        return "denied"


class Authorized(object):
    """Base class for models with a list of authorized users
    """

    def get_actor(self, uid):
        """Retrieve actor associated with this uid.

        Args:
            uid: (str) id of user

        Returns:
            (PActor) or None if no user in auth list
        """
        for actor in self.auth:
            if actor.user == uid:
                return actor

        return None

    def remove_auth(self, session, uid):
        """Remove access granted to user

        Args:
            session: (DBSession)
            uid: (str) id of user or team

        Returns:
            None
        """
        actor = self.get_actor(uid)
        if actor is not None:
            session.delete(actor)

    def update_auth(self, session, uid, new_role):
        """Update role of user.

        Args:
            session: (DBSession)
            parent: (Project[Team)
            uid: (str) user id
            new_role: (Role)

        Returns:
            None
        """
        del session
        actor = self.get_actor(uid)
        actor.role = new_role

