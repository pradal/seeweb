"""Set of functions used to access objects in models
"""
from models.auth import Role
from models.team import Team


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
