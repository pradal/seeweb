from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship

from .actor import UActor
from .models import Base


project_auth = Table('project_auth',
                     Base.metadata,
                     Column('project_id', String(255),
                            ForeignKey('projects.id'),
                            primary_key=True),
                     Column('actor_id', Integer,
                            ForeignKey('uactors.id'),
                            primary_key=True),
                     )


class Project(Base):
    __tablename__ = 'projects'

    id = Column(String(255), unique=True, primary_key=True)
    owner = Column(String(255), ForeignKey("users.id"), nullable=False)

    doc_url = Column(Text, default="")

    public = Column(Boolean)
    auth = relationship("UActor", secondary=project_auth)

    def __repr__(self):
        return "<Project(id='%s', owner='%s', public='%s')>" % (self.id,
                                                                self.owner,
                                                                self.public)

    def add_auth(self, uid, role):
        """Add a new user,role authorization to the project
        """
        actor = UActor(user=uid, role=role)
        self.auth.append(actor)
