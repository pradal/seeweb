from datetime import datetime

from .comment import Comment
from .models import DBSession
from .project import Project
from .team import Team
from .user import User
from .userid import UserId


def create_comment(pid, uid, msg, session=None):
    """Create a new comment now.
    """
    if session is None:
        session = DBSession()

    cmt = Comment(project=pid, author=uid, creation=datetime.now(), message=msg)
    session.add(cmt)

    return cmt


def create_user(uid, name, email, session=None):
    """Create a new user.
    """
    if session is None:
        session = DBSession()

    userid = UserId(id=uid)
    session.add(userid)
    user = User(id=userid.id, name=name, email=email)
    session.add(user)

    return user


def create_project(owner, name, public=False, session=None):
    """Create a new project.

    args:
     - owner (User): future owner of the project
     - name (str): id of the project
     - public (bool): visibility of the project (default False)

    return:
     - (Project): project has been added to user project list
    """
    if session is None:
        session = DBSession()

    project = Project(id=name,
                      owner=owner.id,
                      public=public)
    session.add(project)

    owner.projects.append(project)

    return project


def create_team(tid, session=None):
    """Create a new team.

    Does not test existence of team beforehand
    """
    if session is None:
        session = DBSession()

    team = Team(id=tid)
    session.add(team)

    return team
