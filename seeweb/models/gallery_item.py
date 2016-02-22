import json
from sqlalchemy import Column, ForeignKey, Integer, String, Text

from .described import Described
from .models import Base, get_by_id


class GalleryItem(Base, Described):
    """Base class for gallery items.
    """
    __tablename__ = 'gallery_items'

    id = Column(Integer, autoincrement=True, primary_key=True)
    project = Column(String(255), ForeignKey("projects.id"), nullable=False)
    name = Column(String(255), nullable=False)
    author = Column(String(255), default="")
    url = Column(String(255), default="")

    def __repr__(self):
        tup = (self.id, self.project, self.url)
        return "<GalleryItem(id='%s', project='%s', url='%s')>" % tup

    @staticmethod
    def get(session, cid):
        """Fetch a given item in the database.

        Args:
            session: (DBSession)
            cid: (str) content id

        Returns:
            (GalleryItem) or None if no content with this id is found
        """
        return get_by_id(session, GalleryItem, cid)

    @staticmethod
    def create(session, project, name, url):
        """Create a new gallery item for this project.

        Args:
            session: (DBSession)
            project: (Project)
            name: (str) label to associate to the gallery item
            url: (str) resource the item points to

        Returns:
            (GalleryItem)
        """
        item = GalleryItem(project=project.id, name=name, url=url)
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
        # remove associated resource if in gallery
        pass

        # delete item
        session.delete(item)

        return True
