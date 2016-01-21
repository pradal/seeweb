from datetime import datetime

from .access import fetch_comments
from .comment import Comment
from .fmt import float_to_rating
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


def remove_project(session, project):
    """Remove a given project from the database
    """
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


def create_team(session, tid):
    """Create a new team.

    Does not test existence of team beforehand
    """
    team = Team(id=tid)
    session.add(team)

    return team


def remove_team(session, team):
    """Remove a given team from the database
    """
    # remove authorizations
    for actor in team.auth:
        session.delete(actor)

    # remove team
    session.delete(team)

    return True


def recompute_project_ratings(session, project):
    """Recompute project ratings according to
    comments ratings.
    """
    ratings = dict((name.lower(), [0, 0]) for name, rating in project.format_ratings())

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

    affect_ratings(project, new_ratings)
