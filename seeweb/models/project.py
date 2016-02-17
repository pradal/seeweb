from sqlalchemy import Boolean, Column, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from .auth import Role
from .comment import Comment
from .described import Described
from .models import Base, get_by_id
from .rated import Rated
from .team import Team


class Project(Base, Rated, Described):
    """Basic unit of management.
    """
    __tablename__ = 'projects'

    id = Column(String(255), unique=True, primary_key=True)
    owner = Column(String(255), ForeignKey("users.id"))
    public = Column(Boolean)
    auth = relationship("PActor")

    doc_url = Column(Text, default="")
    doc = Column(Text, default="")

    src_url = Column(Text, default="")

    dependencies = relationship("Dependency")

    def __repr__(self):
        return "<Project(id='%s', owner='%s', public='%s')>" % (self.id,
                                                                self.owner,
                                                                self.public)

    @staticmethod
    def get(session, pid):
        """Fetch a given project in the database.

        Args:
            session: (DBSession)
            pid: (str) project id

        Returns:
            (Project) or None if no project with this id is found
        """
        return get_by_id(session, Project, pid)

    def get_actor(self, uid):
        """Retrieve actor associated with this uid.

        Args:
            uid: (str) id of user

        Returns:
            (PActor) or None if no user in auth list
        """
        for actor in self.auth:
            if actor.user == uid:
                return actor

        return None

    def fetch_comments(self, session, limit=None):
        """Fetch all comments associated to this project.

        Args:
            session: (DBSession)
            limit: (int) maximum number of items to return

        Returns:
            (list of Comment) sorted by score
        """
        query = session.query(Comment).filter(Comment.project == self.id)
        query = query.order_by(Comment.score.desc())
        if limit is not None:
            query = query.limit(limit)

        comments = query.all()

        return comments

    def access_role(self, session, uid):
        """Check the type of access granted to a user.

        Args:
            session: (DBSession)
            uid: id of user to test

        Returns:
            (Role) type of role given to this user
        """
        # user own project
        if self.owner == uid:
            return Role.edit

        # check team auth for this user, supersede sub_team auth
        actor = self.get_actor(uid)
        if actor is not None:
            return actor.role

        if self.public:
            role = Role.view
        else:
            role = Role.denied

        # check team auth in subteams
        for actor in self.auth:
            if actor.is_team:
                team = Team.get(session, actor.user)
                if team.has_member(session, uid):
                    role = max(role, actor.role)
                    # useful in case user is member of multiple teams

        return role
