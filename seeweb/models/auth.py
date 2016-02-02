
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
