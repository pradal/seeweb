"""Set of functions used to edit objects in models
"""
from datetime import datetime

from .avatar import (generate_default_project_avatar,
                     generate_default_team_avatar,
                     generate_default_user_avatar,
                     remove_project_avatar,
                     remove_team_avatar)
from .model_access import fetch_comments
from models.actor import PActor, TActor
from models.comment import Comment
from models.dependency import Dependency
from models.installed import Installed
from models.project import Project
from models.team import Team
from models.user import User
from project.source import delete_source


def create_comment(session, pid, uid, msg, ratings=None):
    """Create a new comment.

    Creation attribute of the comment will be now.

    Args:
        session: (DNSession)
        pid: (str) project id
        uid: (str) user id
        msg: (str) content of the comment
        ratings: (list of (str, float)) ratings proposed by this comment

    Returns:
        (Comment)
    """
    cmt = Comment(project=pid, author=uid, creation=datetime.now(), message=msg)
    session.add(cmt)

    if ratings is not None:
        cmt.affect_ratings(ratings)

    return cmt


def create_user(session, uid, name, email):
    """Create a new user.

    Also create default avatar for this user.

    Args:
        session: (DBSession)
        uid: (str) user id
        name: (str) display name
        email: (str) email address

    Returns:
        (User)
    """
    user = User(id=uid, name=name, email=email)
    session.add(user)

    # create avatar
    generate_default_user_avatar(user)

    return user


def create_project(session, owner_id, name, public=False):
    """Create a new project.

    Also create default avatar for the project.

    Args:
        session: (DBSession)
        owner_id: (uid) id of future owner of the project
        name: (str) id the project
        public: (bool) visibility of the project (default False)

    Returns:
        (Project): project has been added to user project list
    """
    project = Project(id=name,
                      owner=owner_id,
                      public=public)
    session.add(project)

    # create avatar
    generate_default_project_avatar(project)

    return project


def create_team(session, tid):
    """Create a new team.

    Also create default avatar for the team.

    Args:
        session: (DBSession)
        tid: (str) team id

    Returns:
        (Team)
    """
    team = Team(id=tid)
    session.add(team)

    # create avatar
    generate_default_team_avatar(team)

    return team


def remove_user(session, user):
    """Remove a user from database.

    Also remove user's avatar.

    Raises: UserWarning if user still own projects

    Args:
        session: (DBSession)
        user: (User)

    Returns:
        (True)
    """
    # remove avatar
    # TODO

    return True


def remove_project(session, project):
    """Remove a given project from the database.

    Also remove project's avatar and all associated comments.

    Args:
        session: (DBSession)
        project: (Project)

    Returns:
        (True)
    """
    # remove avatar
    remove_project_avatar(project)

    # remove sources
    delete_source(project.id)

    # remove associated comments
    query = session.query(Comment).filter(Comment.project == project.id)
    for comment in query.all():
        session.delete(comment)

    # remove authorizations
    for actor in project.auth:
        session.delete(actor)

    # delete project
    session.delete(project)

    return True


def remove_team(session, team):
    """Remove a given team from the database.

    Also remove team's avatar.

    Args:
        session: (DBSession)
        team: (Team)

    Returns:
        (True)
    """
    # remove avatar
    remove_team_avatar(team)

    # remove authorizations
    for actor in team.auth:
        session.delete(actor)

    # remove team
    session.delete(team)

    return True


def add_project_auth(session, project, user, role):
    """Add a new authorization for this project

    Args:
        session: (DBsession)
        project: (Project)
        user: (User|Team)
        role: (Role) role to grant to user

    Returns:
        None
    """
    actor = PActor(project=project.id, user=user.id, role=role)
    session.add(actor)
    actor.is_team = isinstance(user, Team)


def add_team_auth(session, team, user, role):
    """Add a new authorization for this project

    Args:
        session: (DBsession)
        team: (Team)
        user: (User|Team)
        role: (Role) role to grant to user

    Returns:
        None
    """
    actor = TActor(team=team.id, user=user.id, role=role)
    session.add(actor)
    actor.is_team = isinstance(user, Team)


def remove_auth(session, parent, uid):
    """Remove access granted to user

    Args:
        session: (DBSession)
        parent: (Project|Team)
        uid: (str) id of user or team

    Returns:
        None
    """
    actor = parent.get_actor(uid)
    if actor is not None:
        session.delete(actor)


def update_auth(session, parent, uid, new_role):
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
    actor = parent.get_actor(uid)
    actor.role = new_role


def recompute_project_ratings(session, project):
    """Recompute project ratings from the list of comments.

    Args:
        session: (DBSession)
        project: (Project)

    Returns:
        None
    """
    ratings = dict((name.lower(), [0, 0])
                   for name, rating in project.format_ratings())

    for comment in fetch_comments(session, project.id):
        nb = comment.score
        if nb > 0:
            for name, rating in comment.format_ratings():
                key = name.lower()
                ratings[key][0] += nb
                ratings[key][1] += rating * nb

    new_ratings = []
    for key, (nb, val) in ratings.items():
        if nb == 0:
            rating = 2.5
        else:
            rating = val / nb
        new_ratings.append((key, rating))

    project.affect_ratings(new_ratings)


def add_dependency(session, project, name, version):
    """Add a new dependency for the project

    Args:
        session: (DBSession)
        project: (Project)
        name: (str) name of project|package
        version: (str) version min to use

    Returns:
        (None)
    """
    dep = Dependency(project=project.id, name=name, version=version)
    session.add(dep)


def install_project(session, user, project):
    """Install project in user installed projects

    Warnings: Does not test if user has permission to do that.

    Args:
        session: (DBSession)
        user: (User)
        project: (Project)

    Returns:
        None
    """
    installed = Installed(user=user.id,
                          project=project.id,
                          date=datetime.now(),
                          version="0.0.0")
    session.add(installed)


def uninstall_project(session, user, project):
    """Uninstall project from user installed projects

    Raises: UserWarning if project is not installed

    Args:
        session: (DBSession)
        user: (User)
        project: (Project)

    Returns:
        None
    """
    for installed in user.installed:
        if installed.project == project.id:
            session.delete(installed)
            return
