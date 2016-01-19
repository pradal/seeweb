from datetime import datetime

from .comment import Comment
from .project import Project
from .team import Team
from .user import User


def create_comment(session, pid, uid, msg, ratings):
    """Create a new comment now.
    """
    cmt = Comment(project=pid, author=uid, creation=datetime.now(), message=msg)
    session.add(cmt)

    return cmt


def create_user(session, uid, name, email):
    """Create a new user.
    """
    user = User(id=uid, name=name, email=email)
    session.add(user)

    return user


def create_project(session, owner_id, name, public=False):
    """Create a new project.

    args:
     - owner_id (uid): id of future owner of the project
     - name (str): id of the project
     - public (bool): visibility of the project (default False)

    return:
     - (Project): project has been added to user project list
    """
    project = Project(id=name,
                      owner=owner_id,
                      public=public)
    session.add(project)

    # owner.projects.append(project)

    return project


def create_team(session, tid):
    """Create a new team.

    Does not test existence of team beforehand
    """
    team = Team(id=tid)
    session.add(team)

    return team
