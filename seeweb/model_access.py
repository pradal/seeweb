"""Set of functions used to access objects in models
"""
from models.auth import Role
from models.team import Team


def is_contributor(session, project, uid):
    """Check whether project has a given member.

    Also check sub teams recursively.

    Args:
        session: (DBSession)
        project: (Project)
        uid: (str) user id

    Returns:
        (Bool) True if user is appears in the project or one
        of the teams in the project recursively and its role is not
        'denied'.
    """
    actors = list(project.auth)
    while len(actors) > 0:
        actor = actors.pop(0)
        if actor.user == uid:
            return actor.role != Role.denied

        if actor.is_team:
            actors.extend(Team.get(session, actor.user).auth)

    return False


def project_access_role(session, project, uid):
    """Check the type of access granted to a user for a given project.

    Args:
        session: (DBSession)
        project: (Project)
        uid: id of user to test

    Returns:
        (Role) type of role given to this user
    """
    # user own project
    if project.owner == uid:
        return Role.edit

    # check team auth for this user, supersede sub_team auth
    actor = project.get_actor(uid)
    if actor is not None:
        return actor.role

    if project.public:
        role = Role.view
    else:
        role = Role.denied

    # check team auth in subteams
    for actor in project.auth:
        if actor.is_team:
            team = Team.get(session, actor.user)
            if team.has_member(session, uid):
                role = max(role, actor.role)
                # useful in case user is member of multiple teams

    return role


def team_access_role(session, team, uid):
    """Check the type of access granted to a user for a given team.

    Args:
        session: (DBSession)
        team: (Team)
        uid: id of user to test

    Returns:
        (Role) type of role given to this user
    """
    # check team auth for this user, supersede sub_team auth
    actor = team.get_actor(uid)
    if actor is not None:
        return actor.role

    # check team auth in subteams
    role = Role.view  # teams are public by default

    for actor in team.auth:
        if actor.is_team:
            team = Team.get(session, actor.user)
            if team.has_member(session, uid):
                role = max(role, actor.role)
                # useful in case user is member of multiple teams

    return role
