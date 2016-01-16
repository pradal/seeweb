from datetime import datetime

from .comment import Comment
from .models import DBSession
from .project import Project
from .team import Team


def create_project(owner, name, public=False):
    """Create a new project.

    args:
     - owner (User): future owner of the project
     - name (str): id of the project
     - public (bool): visibility of the project (default False)

    return:
     - (Project): project has been added to user project list
    """
    project = Project(id=name,
                      owner=owner.id,
                      public=public)

    owner.projects.append(project)

    return project


def register_project(owner, pid):
    """Create a new project and register it.
    """
    session = DBSession()
    project = create_project(owner, pid, public=False)
    session.add(project)

    return project


def create_team(tid):
    """Create a new team.

    Does not test existence of team beforehand
    """
    team = Team(id=tid)

    return team


def register_team(tid):
    """Create a new team.

    Does not test existence of team beforehand
    """
    session = DBSession()
    team = create_team(tid)
    session.add(team)

    return team


def create_comment(pid, uid, msg):
    """Create a new comment now.
    """
    cmt = Comment(project=pid, author=uid, creation=datetime.now(), message=msg)

    return cmt
