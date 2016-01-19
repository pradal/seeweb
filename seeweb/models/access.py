from .auth import Role
from .comment import Comment
from .project import Project
from .team import Team
from .user import User


def get_comment(session, cid):
    """Fetch a given comment from the database
    """
    comments = session.query(Comment).filter(Comment.id == cid).all()
    if len(comments) == 0:
        return None

    comment, = comments

    return comment


def get_project(session, pid):
    """Fetch a given project in the database
    """
    projects = session.query(Project).filter(Project.id == pid).all()
    if len(projects) == 0:
        return None

    project, = projects

    return project


def get_team(session, tid):
    """Fetch a given team from the database
    """
    teams = session.query(Team).filter(Team.id == tid).all()
    if len(teams) == 0:
        return None

    team, = teams

    return team


def get_user(session, uid):
    """Fetch a given user from the database
    """
    users = session.query(User).filter(User.id == uid).all()
    if len(users) == 0:
        return None

    user, = users

    return user


def fetch_comments(session, pid, limit=None):
    """Fectch all comments associated to a project.
    """
    query = session.query(Comment).filter(Comment.project == pid)
    query = query.order_by(Comment.score.desc())
    if limit is not None:
        query = query.limit(limit)

    comments = query.all()

    return comments


def is_member(session, team, uid):
    """Check whether team has a given member.

    Also check sub teams
    """
    actors = list(team.auth)
    while len(actors) > 0:
        actor = actors.pop(0)
        if actor.user == uid:
            return actor.role != Role.denied  # potential problem here, better ensure Role.denied never occurs

        if actor.is_team:
            actors.extend(get_team(session, actor.user).auth)

    return False


def is_contributor(session, project, uid):
    """Check whether project has a given member.

    Also check sub teams
    """
    actors = list(project.auth)
    while len(actors) > 0:
        actor = actors.pop(0)
        if actor.user == uid:
            return actor.role != Role.denied  # potential problem here, better ensure Role.denied never occurs

        if actor.is_team:
            actors.extend(get_team(session, actor.user).auth)

    return False


def project_access_role(session, project, uid):
    """Check the type of access granted to a user for a given project.

    args:
     - project (Project): project to check
     - uid (str): id of user willing to access project

    return:
     - role (Role): type of access granted to user
     - project (Project): project associated to pid
    """
    # user own project
    if project.owner == uid:
        return Role.edit

    # check team auth for this user, supersede sub_team auth
    actor = project.get_actor(uid)
    if actor is not None:
        return actor.role

    if project.public:
        role = Role.read
    else:
        role = Role.denied

    # check team auth in subteams
    for actor in project.auth:
        if actor.is_team:
            tid = actor.user
            if is_member(session, get_team(session, tid), uid):
                role = max(role, actor.role)

    return role


def team_access_role(session, team, uid):
    """Check the type of access granted to a user for a given team.

    args:
     - team (Team): team to check
     - uid (str): id of user willing to access team

    return:
     - role (Role): type of access granted to user
    """
    # check team auth for this user, supersede sub_team auth
    actor = team.get_actor(uid)
    if actor is not None:
        return actor.role

    # check team auth in subteams
    role = Role.read

    for actor in team.auth:
        if actor.is_team:
            tid = actor.user
            if is_member(session, get_team(session, tid), uid):
                role = max(role, actor.role)

    # teams are public by default
    return role
