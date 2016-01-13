
class Role(object):
    denied = 0
    read = 1
    edit = 2


def access_role(project, username):
    """Check the type of access granted to a user.

    args:
     - project (Project): project to test
     - username (str): id of user willing to access project

    return:
     - role (Role): type of access granted to user
    """
    # user own project
    if project.owner == username:
        return Role.edit

    # project is public
    if project.public:
        return Role.read
    else:
        return Role.denied
