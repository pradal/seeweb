from datetime import datetime

from comment import Comment
from project import Project
from team import Team


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


def create_team(tid, public=False):
    """Create a new team.

    Does not test existence of team beforehand
    """
    team = Team(id=tid, public=public)

    return team


def create_comment(pid, uid, msg):
    """Create a new comment now.
    """
    cmt = Comment(project=pid, author=uid, creation=datetime.now(), message=msg)

    return cmt
