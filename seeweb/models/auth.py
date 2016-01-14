
class Role(object):
    denied = 0
    read = 1
    edit = 2

    @staticmethod
    def from_str(role_str):
        if role_str == "edit":
            return Role.edit

        if role_str == "read":
            return Role.read

        return Role.denied

    @staticmethod
    def to_str(role):
        if role == Role.edit:
            return "edit"

        if role == Role.read:
            return "read"

        return "denied"
