"""Set of functions used to access objects in models
"""
from models.auth import Role
from models.comment import Comment
from models.project import Project
from models.project_content.content import Content
from models.project_content.workflow import Workflow
from models.project_content.workflow_node import WorkflowNode
from models.team import Team
from models.user import User


def _get_by_id(session, object_type, obj_id):
    """Internal function used to retrieve an object from
    the database using its id.

    Args:
        session: (DBSession)
        object_type: (Class)
        obj_id: (any)

    Returns:
        (Object or None) if no object found
    """
    if obj_id is None:
        return None

    items = session.query(object_type).filter(object_type.id == obj_id).all()
    if len(items) == 0:
        return None

    item, = items

    return item


def get_comment(session, cid):
    """Fetch a given comment from the database.

    Args:
        session: (DBSession)
        cid: (int) comment id

    Returns:
        (Comment) or None if no comment with this id is found
    """
    return _get_by_id(session, Comment, cid)


def get_project(session, pid):
    """Fetch a given project in the database.

    Args:
        session: (DBSession)
        pid: (str) project id

    Returns:
        (Project) or None if no project with this id is found
    """
    return _get_by_id(session, Project, pid)


def get_project_content(session, pid):
    """Fetch the content of a given project in the database.

    Args:
        session: (DBSession)
        pid: (str) project id

    Returns:
        (Content) or None if no project with this id is found
    """
    return _get_by_id(session, Content, pid)


def get_team(session, tid):
    """Fetch a given team in the database.

    Args:
        session: (DBSession)
        tid: (str) team id

    Returns:
        (Team) or None if no team with this id is found
    """
    return _get_by_id(session, Team, tid)


def get_user(session, uid):
    """Fetch a given user in the database.

    Args:
        session: (DBSession)
        uid: (str) user id

    Returns:
        (User) or None if no user with this id is found
    """
    return _get_by_id(session, User, uid)


def get_workflow(session, wid):
    """Fetch a given workflow in the database.

    Args:
        session: (DBSession)
        wid: (str) workflow id

    Returns:
        (Workflow) or None if no workflow with this id is found
    """
    return _get_by_id(session, Workflow, wid)


def get_workflow_node(session, nid):
    """Fetch a given workflow node in the database.

    Args:
        session: (DBSession)
        nid: (str) workflow node id

    Returns:
        (WorkflowNode) or None if no node with this id is found
    """
    return _get_by_id(session, WorkflowNode, nid)


def fetch_comments(session, pid, limit=None):
    """Fetch all comments associated to a project.

    Args:
        session: (DBSession)
        pid: (str) project id
        limit: (int) maximum number of items to return

    Returns:
        (list of Comment) sorted by score
    """
    query = session.query(Comment).filter(Comment.project == pid)
    query = query.order_by(Comment.score.desc())
    if limit is not None:
        query = query.limit(limit)

    comments = query.all()

    return comments


def is_member(session, team, uid):
    """Check whether team has a given member.

    Also check sub teams recursively.

    Args:
        session: (DBSession)
        team: (Team)
        uid: (str) user id

    Returns:
        (Bool) True if user is appears in the team or one
        of the sub teams recursively and its role is not
        'denied'.
    """
    actors = list(team.auth)
    while len(actors) > 0:
        actor = actors.pop(0)
        if actor.user == uid:
            return actor.role != Role.denied

        if actor.is_team:
            actors.extend(get_team(session, actor.user).auth)

    return False


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
            actors.extend(get_team(session, actor.user).auth)

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
            tid = actor.user
            if is_member(session, get_team(session, tid), uid):
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
            tid = actor.user
            if is_member(session, get_team(session, tid), uid):
                role = max(role, actor.role)
                # useful in case user is member of multiple teams

    return role


def is_installed(session, user, project):
    """Check whether the project has already been installed for this user

    Args:
        session: (DBSession)
        user: (User)
        project: (Project)

    Returns:
        (bool): True if project already in user installed list
    """
    del session

    for installed in user.installed:
        if installed.project == project.id:
            return True

    return False
