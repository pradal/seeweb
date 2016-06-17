from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from seeweb.avatar import (generate_default_ro_avatar,
                           remove_ro_avatar)

from .auth import Authorized, Role, ROPolicy
from .described import Described
from .models import Base, get_by_id


class ResearchObject(Base, Described, Authorized):
    """Base class for all research objects
    """
    __tablename__ = 'ros'

    id = Column(String(32), nullable=False, primary_key=True)
    type = Column(String(50))

    creator = Column(String(255), ForeignKey("users.id"))
    created = Column(DateTime, nullable=False)

    version = Column(Integer, nullable=False)
    title = Column(Text, default="")

    auth = relationship("ROPolicy")

    remote = Column(Text, default="")

    out_links = relationship("ROLink", foreign_keys="ROLink.source")
    in_links = relationship("ROLink", foreign_keys="ROLink.target")

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'ro'
    }

    def __repr__(self):
        return "<RO(id='%s', title='%s', version='%d')>" % (self.id,
                                                            self.title,
                                                            self.version)

    @staticmethod
    def get(session, uid):
        """Fetch a given RO in the database.

        Args:
            session: (DBSession)
            uid: (str) RO id

        Returns:
            (ResearchObject) or None if no RO with this id is found
        """
        return get_by_id(session, ResearchObject, uid)

    @staticmethod
    def create(session, uid, creator_id, title):
        """Create a new RO.

        Also create default avatar for this user.

        Args:
            session: (DBSession)
            uid: (str) unique id for RO
            creator_id: (str) id of actor creating the object
            title: (str) name of this RO

        Returns:
            (ResearchObject)
        """
        created = datetime.now()
        version = 0

        ro = ResearchObject(id=uid,
                            creator=creator_id, created=created,
                            version=version,
                            title=title)
        session.add(ro)

        # create avatar
        generate_default_ro_avatar(ro)

        return ro

    @staticmethod
    def remove(session, ro, recursive):
        """Remove a RO from database.

        Args:
            session: (DBSession)
            ro: (ResearchObject)
            recursive: (bool) whether to also remove ROs contained in this RO

        Returns:
            (True)
        """
        # remove avatar
        remove_ro_avatar(ro)

        # remove authorizations
        for pol in ro.auth:
            session.delete(pol)

        # remove all links
        ros = []
        for link in ro.out_links:
            if link.type == "contains":
                ros.append(link.target)
            session.delete(link)
        for link in ro.in_links:
            session.delete(link)

        # remove RO
        session.delete(ro)

        # recursivity
        if recursive:
            for uid in ros:
                ro = ResearchObject.get(session, uid)
                if ro.is_lonely():
                    ResearchObject.remove(session, ro, recursive)

        return True

    def add_policy(self, session, actor, role):
        """Add a new authorization policy for this team

        Args:
            session: (DBSession)
            actor: (Actor)
            role: (Role) role to grant to user

        Returns:
            None
        """
        actor = ROPolicy(ro=self.id, actor=actor.id, role=role)
        session.add(actor)

    def access_role(self, session, uid):
        """Check the type of access granted to an actor.

        Args:
            session: (DBSession)
            uid: id of actor to test

        Returns:
            (Role) type of role given to this actor
        """
        if uid == self.creator:
            return Role.edit

        # check local auth for this actor, supersede any parent auth
        pol = self.get_policy(uid)
        if pol is not None:
            return pol.role

        # check containers of this object
        for link in self.in_links:
            if link.type == "contains":
                container = ResearchObject.get(session, link.source)
                container_role = container.access_role(session, uid)
                if container_role is not None:
                    return container_role

        return Role.denied

    def is_lonely(self):
        """Check whether this RO is inside another one

        Returns:
            (bool): True if no other RO is linked to this one through a
                    'contains' link
        """
        conts = [1 for link in self.in_links if link.type == "contains"]
        return len(conts) == 0
