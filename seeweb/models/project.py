from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship

from .actor import PActor
from .models import Base, DBSession


class Project(Base):
    __tablename__ = 'projects'

    id = Column(String(255), unique=True, primary_key=True)
    owner = Column(String(255), ForeignKey("users.id"))

    doc_url = Column(Text, default="")

    public = Column(Boolean)
    auth = relationship("PActor")

    def __repr__(self):
        return "<Project(id='%s', owner='%s', public='%s')>" % (self.id,
                                                                self.owner,
                                                                self.public)

    def get_actor(self, uid):
        """Retrieve actor associated with this uid.
        """
        for i, actor in enumerate(self.auth):
            if actor.user == uid:
                return i, actor

        return None, None

    def add_auth(self, uid, role):
        """Add a new user,role authorization to the project
        """
        session = DBSession()
        actor = PActor(project=self.id, user=uid, role=role)
        session.add(actor)
