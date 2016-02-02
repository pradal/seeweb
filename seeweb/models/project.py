from sqlalchemy import Boolean, Column, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from .described import Described
from .models import Base
from .rated import Rated


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

    def __repr__(self):
        return "<Project(id='%s', owner='%s', public='%s')>" % (self.id,
                                                                self.owner,
                                                                self.public)

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
