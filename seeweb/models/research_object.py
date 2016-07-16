from datetime import datetime
import json
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer,
                        String, Text)
from sqlalchemy.orm import relationship
from uuid import uuid1

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

    owner = Column(String(255), ForeignKey("users.id"))
    created = Column(DateTime, nullable=False)

    version = Column(Integer, nullable=False)
    name = Column(Text, default="")

    remote = Column(Text, default="")
    definition = Column(Text, default="{}")

    public = Column(Boolean, default=False)
    auth = relationship("ROPolicy")

    out_links = relationship("ROLink", foreign_keys="ROLink.source")
    in_links = relationship("ROLink", foreign_keys="ROLink.target")

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'ro'
    }

    def __repr__(self):
        return "<RO(id='%s', name='%s', version='%d')>" % (self.id,
                                                           self.name,
                                                           self.version)

    def init(self, session, ro_def):
        """Initialize this RO with a set of attributes

        Args:
            session (DBSession):
            ro_def (dict): set of properties to initialize this RO

        Returns:
            None
        """
        if "id" in ro_def:
            self.id = ro_def['id']
        else:
            self.id = uuid1().hex

        self.owner = ro_def.get("owner", "unknown")
        if "created" in ro_def:
            self.created = ro_def['created']
        else:
            self.created = datetime.now()

        self.version = 0

        self.name = ro_def.get('name', "no name")

        self.remote = ro_def.get('remote', "")

        if 'description' in ro_def:
            self.store_description(ro_def['description'])

        self.store_definition(ro_def)

        # add RO to database
        session.add(self)

        # create avatar
        generate_default_ro_avatar(self)

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
        if uid == self.owner:
            return Role.edit

        # check local auth for this actor, supersede any parent auth
        pol = self.get_policy(uid)
        if pol is not None:
            return pol.role

        # check containers of this object
        if self.public:
            role = Role.view
        else:
            role = Role.denied
        for link in self.in_links:
            if link.type == "contains":
                container = ResearchObject.get(session, link.source)
                role = max(role, container.access_role(session, uid))

        return role

    def change_owner(self, session, user):
        """Change ownership of the RO

        Args:
            session: (DBSession)
            user: (User) new owner for the project

        Returns:
            (None)
        """
        del session
        self.owner = user.id

    def is_lonely(self):
        """Check whether this RO is inside another one

        Returns:
            (bool): True if no other RO is linked to this one through a
                    'contains' link
        """
        conts = [1 for link in self.in_links if link.type == "contains"]
        return len(conts) == 0

    def store_definition(self, ro_def):
        """Serialize obj in json format to store it as def.

        Notes: remove attributes in obj which are already stored as attributes
               of RO

        Args:
            ro_def (dict): dict of RO properties, each property must be json
                           serializable

        Returns:
            None
        """
        loc_def = dict(ro_def)
        for key in ('id', 'type',
                    'owner', 'created',
                    'version', 'name',
                    'remote'):
            loc_def.pop(key, None)

        self.definition = json.dumps(loc_def, sort_keys=True)

    def load_definition(self):
        """Load previously stored definition.

        Notes: Attributes which are directly stored as attributes of RO are
               not loaded back into the returned object.

        Returns:
            (dict): RO properties previously stored
        """
        return json.loads(self.definition)

    def repr_json(self, full=False):
        """Create a json representation of this object

        Args:
            full (bool): if True, also add all properties stored in definition
                         default False

        Returns:
            dict
        """
        d = dict(id=self.id,
                 type=self.type,
                 owner=self.owner,
                 created=self.created.isoformat(),
                 version=self.version,
                 name=self.name,
                 remote=self.remote)

        if full:
            d.update(self.load_definition())

        return d
