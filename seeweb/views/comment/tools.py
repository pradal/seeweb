from seeweb.models import DBSession
from seeweb.models.comment import Comment


def get_comment(cid):
    session = DBSession()

    comments = session.query(Comment).filter(Comment.id == cid).all()
    if len(comments) == 0:
        return None

    project, = comments

    return project
