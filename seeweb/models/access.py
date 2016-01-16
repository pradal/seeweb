from .comment import Comment
from .models import DBSession
from .project import Project
from .team import Team
from .user import User


def get_project(pid):
    """Fetch a given project in the database
    """
    session = DBSession()

    projects = session.query(Project).filter(Project.id == pid).all()
    if len(projects) == 0:
        return None

    project, = projects

    return project


def get_team(tid):
    """Fetch a given team from the database
    """
    session = DBSession()
    teams = session.query(Team).filter(Team.id == tid).all()
    if len(teams) == 0:
        return None

    team, = teams

    return team


def get_user(uid):
    """Fetch a given user from the database
    """
    session = DBSession()
    users = session.query(User).filter(User.id == uid).all()
    if len(users) == 0:
        return None

    user, = users

    return user


def fetch_comments(pid, limit=None):
    """Fectch all comments associated to a project.
    """
    session = DBSession()

    query = session.query(Comment).filter(Comment.project == pid).order_by(Comment.rating.desc())
    if limit is not None:
        query = query.limit(limit)

    comments = query.all()

    return comments

