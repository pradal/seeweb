from actor import Actor


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

    # check project auth for this user
    for actor in project.auth:
        if actor.user == username:
            return actor.role

    # project is public
    if project.public:
        return Role.read
    else:
        return Role.denied


def add_auth(project, username, role):
    """Add a new user,role authorization to the project
    """
    actor = Actor(user=username, role=role)
    project.auth.append(actor)


def add_member(team, username, role):
    """Add a new user to the team
    """
    actor = Actor(user=username, role=role)
    team.auth.append(actor)
