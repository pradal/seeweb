import json
from sqlalchemy import Column, ForeignKey, String, Text

from .described import Described
from .models import Base, get_by_id


class ContentItem(Base, Described):
    """Base class for content items.
    """
    __tablename__ = 'pjt_content_items'

    id = Column(String(32), nullable=False, primary_key=True)
    category = Column(String(255), nullable=False)
    project = Column(String(255), ForeignKey("projects.id"), nullable=False)
    name = Column(String(255), nullable=False)
    author = Column(String(255), default="")
    definition = Column(Text, default="")

    def __repr__(self):
        tup = (self.id, self.category, self.project)
        return "<ContentItem(id='%s', category='%s', project='%s')>" % tup

    @staticmethod
    def get(session, cid):
        """Fetch a given item in the database.

        Args:
            session: (DBSession)
            cid: (str) content id

        Returns:
            (ContentItem) or None if no content with this id is found
        """
        return get_by_id(session, ContentItem, cid)

    @staticmethod
    def create(session, cid, category, project):
        """Create a new content item for this project.

        Args:
            session: (DBSession)
            cid: (uuid) id of the content
            category: (str)
            project: (Project) project that will own the content

        Returns:
            (ContentItem)
        """
        item = ContentItem(id=cid,
                           category=category,
                           project=project.id)
        session.add(item)

        return item

    @staticmethod
    def remove(session, item):
        """Remove a given item from the database.

        Args:
            session: (DBSession)
            item: (ContentItem)

        Returns:
            (True)
        """
        # delete project
        session.delete(item)

        return True

    def store_definition(self, obj):
        """Serialize obj in json format to store it as def.

        Args:
            obj: (any) any json serializable object

        Returns:
            None
        """
        self.definition = json.dumps(obj)

    def load_definition(self):
        """Load previously stored definition.

        Returns:
            (any): any json serialized object stored.
        """
        if self.definition == "":
            return None

        return json.loads(self.definition)
