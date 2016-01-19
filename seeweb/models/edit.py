from datetime import datetime

from .fmt import float_to_rating
from .comment import Comment
from .project import Project
from .team import Team
from .user import User


def affect_ratings(rated, ratings):
    """Affect ratings to an object.

    Inverse of 'format_ratings' function.
    """
    ratings = dict((name.lower(), rating) for name, rating in ratings)
    rated.rating_value = float_to_rating(ratings["value"])
    rated.rating_doc = float_to_rating(ratings["documentation"])
    rated.rating_install = float_to_rating(ratings["installation"])
    rated.rating_usage = float_to_rating(ratings["usage"])


def create_comment(session, pid, uid, msg, ratings=None):
    """Create a new comment now.
    """
    cmt = Comment(project=pid, author=uid, creation=datetime.now(), message=msg)
    session.add(cmt)

    if ratings is not None:
        affect_ratings(cmt, ratings)

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
