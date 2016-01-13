from actor import Actor


class Role(object):
    denied = 0
    read = 1
    edit = 2


def access_role(project, uid):
    """Check the type of access granted to a user.

    args:
     - project (Project): project to test
     - uid (str): id of user willing to access project

    return:
     - role (Role): type of access granted to user
    """
    # user own project
    if project.owner == uid:
        return Role.edit

    # check project auth for this user
    for actor in project.auth:
        if actor.user == uid:
            return actor.role

    # project is public
    if project.public:
        return Role.read
    else:
        return Role.denied


def add_auth(project, uid, role):
    """Add a new user,role authorization to the project
    """
    actor = Actor(user=uid, role=role)
    project.auth.append(actor)


def add_member(team, uid, role):
    """Add a new user to the team
    """
    actor = Actor(user=uid, role=role)
    team.auth.append(actor)
