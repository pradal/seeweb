from os import mkdir, remove
from os.path import dirname, exists
from os.path import join as pj
from PIL import Image
from sqlalchemy import Column, ForeignKey, Integer, String

from seeweb.io import rmtree

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
    def gallery_pth(project):
        """Return the path to the gallery of images associated with a project.

        Warnings: does not test if path exists

        Args:
            project: (str) project id

        Returns:
            (str): pth to gallery dir
        """
        root = dirname(dirname(__file__))

        return pj(root, "data", "gallery", project)

    @staticmethod
    def delete_gallery(project):
        """Remove all images from gallery.

        Args:
            project: (Project)

        Returns:
            (None)
        """
        gal_dir = GalleryItem.gallery_pth(project.id)
        if exists(gal_dir):
            rmtree(gal_dir)

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
    def create_gallery_image(session, project, img, img_name):
        """Save a new image in the gallery of a project.

        Args:
            session: (DBSession)
            project: (Project)
            img: (Image)
            img_name: (str) name to use to store image

        Returns:
            None
        """
        gal_dir = GalleryItem.gallery_pth(project.id)
        if not exists(gal_dir):
            mkdir(gal_dir)

        img_pth = pj(gal_dir, img_name)
        if exists(img_pth):
            remove(img_pth)

        img.save(img_pth)

        # create gallery item
        url = "seeweb:data/gallery/%s/%s" % (project.id, img_name)
        item = GalleryItem.create(session, project, img_name, url)
        item.author = project.owner
        session.flush()

        # thumbnail
        item.upload_gallery_thumbnail(img)

    @staticmethod
    def remove(session, item):
        """Remove a given item from the database.

        Args:
            session: (DBSession)
            item: (ContentItem)

        Returns:
            (True)
        """
        pth = GalleryItem.gallery_pth(item.project)

        # remove associated thumbnail
        thumb_pth = pj(pth, "%s_thumb.png" % item.id)
        if exists(thumb_pth):
            remove(thumb_pth)

        # remove associated resource if in gallery
        if item.url.startswith("seeweb:"):
            img_name = item.url.split("/")[-1]
            img_pth = pj(pth, img_name)
            if exists(img_pth):
                remove(img_pth)

        # delete item
        session.delete(item)

        return True

    def upload_gallery_thumbnail(self, img):
        """Convert image to thumbnail and save it for item

        Args:
            img: (Image)

        Returns:
            None
        """
        gal_dir = GalleryItem.gallery_pth(self.project)
        if not exists(gal_dir):
            mkdir(gal_dir)

        # thumbnail
        s = 256
        thumb = Image.new('RGBA', (s, s))
        img.thumbnail((s, s))
        thumb.paste(img, ((s - img.size[0]) / 2, (s - img.size[1]) / 2))

        th_name = "%s_thumb.png" % self.id
        th_pth = pj(gal_dir, th_name)
        if exists(th_pth):
            remove(th_pth)

        thumb.save(th_pth)
