from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from .models import Base, get_by_id
from .rated import Rated


class Comment(Base, Rated):
    """Comment written by a user and associated with a project
    """
    __tablename__ = 'comments'

    id = Column(Integer, autoincrement=True, primary_key=True)
    project = Column(String(255), ForeignKey("projects.id"), nullable=False)
    author = Column(String(255), ForeignKey("users.id"), nullable=False)
    creation = Column(DateTime, nullable=False)

    message = Column(Text, default="")
    score = Column(Integer, default=1)  # TODO list of vote objects to avoid multiple same voters

    def __repr__(self):
        return "<Comment(id='%s')>" % self.id

    @staticmethod
    def create(session, pid, uid, msg, ratings=None):
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

    @staticmethod
    def get(session, cid):
        """Fetch a given comment from the database.

        Args:
            session: (DBSession)
            cid: (int) comment id

        Returns:
            (Comment) or None if no comment with this id is found
        """
        return get_by_id(session, Comment, cid)


