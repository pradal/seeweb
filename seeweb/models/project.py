from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship

from .actor import Actor
from .auth import Role
from .models import Base


project_auth = Table('project_auth',
                     Base.metadata,
                     Column('project_id', String(255),
                            ForeignKey('projects.id'),
                            primary_key=True),
                     Column('actor_id', Integer,
                            ForeignKey('actors.id'),
                            primary_key=True),
                     )


class Project(Base):
    __tablename__ = 'projects'

    id = Column(String(255), unique=True, primary_key=True)
    owner = Column(String(255), ForeignKey("users.id"), nullable=False)

    doc_url = Column(Text, default="")

    public = Column(Boolean)
    auth = relationship("Actor", secondary=project_auth)

    def __repr__(self):
        return "<Project(id='%s', owner='%s', public='%s')>" % (self.id,
                                                                self.owner,
                                                                self.public)

    def add_auth(self, uid, role):
        """Add a new user,role authorization to the project
        """
        actor = Actor(user=uid, role=role)
        self.auth.append(actor)

    def access_role(self, uid):
        """Check the type of access granted to a user.

        args:
         - uid (str): id of user willing to access project

        return:
         - role (Role): type of access granted to user
        """
        # user own project
        if self.owner == uid:
            return Role.edit

        # check project auth for this user
        for actor in self.auth:
            if actor.user == uid:
                return actor.role

        # project is public
        if self.public:
            return Role.read
        else:
            return Role.denied
