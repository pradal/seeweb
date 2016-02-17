from sqlalchemy import Boolean, Column, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from seeweb.avatar import (generate_default_project_avatar,
                           remove_project_avatar)
from seeweb.project.source import delete_source

from .actor import PActor
from .auth import Authorized, Role
from .comment import Comment
from .dependency import Dependency
from .described import Described
from .models import Base, get_by_id
from .rated import Rated
from .team import Team


class Project(Base, Rated, Described, Authorized):
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

    @staticmethod
    def create(session, owner_id, name, public=False):
        """Create a new project.

        Also create default avatar for the project.

        Args:
            session: (DBSession)
            owner_id: (uid) id of future owner of the project
            name: (str) id the project
            public: (bool) visibility of the project (default False)

        Returns:
            (Project): project has been added to user project list
        """
        project = Project(id=name,
                          owner=owner_id,
                          public=public)
        session.add(project)

        # create avatar
        generate_default_project_avatar(project)

        return project

    @staticmethod
    def remove(session, project):
        """Remove a given project from the database.

        Also remove project's avatar and all associated comments.

        Args:
            session: (DBSession)
            project: (Project)

        Returns:
            (True)
        """
        # remove avatar
        remove_project_avatar(project)

        # remove sources
        delete_source(project.id)

        # remove associated comments
        query = session.query(Comment).filter(Comment.project == project.id)
        for comment in query.all():
            session.delete(comment)

        # remove authorizations
        for actor in project.auth:
            session.delete(actor)

        # remove dependencies
        for dep in project.dependencies:
            session.delete(dep)

        # delete project
        session.delete(project)

        return True

    def add_auth(self, session, user, role):
        """Add a new authorization for this project

        Args:
            session: (DBsession)
            user: (User|Team)
            role: (Role) role to grant to user

        Returns:
            None
        """
        actor = PActor(project=self.id, user=user.id, role=role)
        session.add(actor)
        actor.is_team = isinstance(user, Team)

    def add_dependency(self, session, name, version):
        """Add a new dependency for the project

        Args:
            session: (DBSession)
            name: (str) name of project|package
            version: (str) version min to use

        Returns:
            (None)
        """
        dep = Dependency(project=self.id, name=name, version=version)
        session.add(dep)

    def change_owner(self, session, user):
        """Change ownership of the project

        Args:
            session: (DBSession)
            user: (User) new owner for the project

        Returns:
            (None)
        """
        del session
        self.owner = user.id

    def clear_dependencies(self, session):
        """Remove all dependencies from the project

        Args:
            session: (DBSession)

        Returns:
            (None)
        """
        for dep in list(self.dependencies):
            session.delete(dep)

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
