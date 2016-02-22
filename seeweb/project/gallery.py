"""Set of functions used to manage galleries
"""
import os
from os.path import dirname, exists, join
from PIL import Image

from seeweb.io import rmtree
from seeweb.models.gallery_item import GalleryItem


def gallery_pth(project):
    """Return the path to the gallery of images associated with a project.

    Warnings: does not test if path exists

    Args:
        project: (str) project id

    Returns:
        (str): pth to gallery dir
    """
    root = dirname(dirname(__file__))

    return join(root, "data", "gallery", project)


def delete_gallery(project):
    """Remove all images from gallery.

    Args:
        project: (Project)

    Returns:
        (None)
    """
    gal_dir = gallery_pth(project.id)
    if exists(gal_dir):
        rmtree(gal_dir)


def upload_gallery_thumbnail(img, item):
    """Convert image to thumbnail and save it for item

    Args:
        img: (Image)
        item: (GalleryItem)

    Returns:
        None
    """
    gal_dir = gallery_pth(item.project)
    if not exists(gal_dir):
        os.mkdir(gal_dir)

    # thumbnail
    s = 256
    thumb = Image.new('RGBA', (s, s))
    img.thumbnail((s, s))
    thumb.paste(img, ((s - img.size[0]) / 2, (s - img.size[1]) / 2))

    th_name = "%s_thumb.png" % item.id
    th_pth = join(gal_dir, th_name)
    if exists(th_pth):
        os.remove(th_pth)

    thumb.save(th_pth)


def add_gallery_image(session, project, img, img_name):
    """Save a new image in the gallery of a project.

    Args:
        session: (DBSession)
        project: (Project)
        img: (Image)
        img_name: (str) name to use to store image

    Returns:
        None
    """
    gal_dir = gallery_pth(project.id)
    if not exists(gal_dir):
        os.mkdir(gal_dir)

    img_pth = join(gal_dir, img_name)
    if exists(img_pth):
        os.remove(img_pth)

    img.save(img_pth)

    # create gallery item
    url = "seeweb:data/gallery/%s/%s" % (project.id, img_name)
    item = GalleryItem.create(session, project, img_name, url)
    item.author = project.owner
    session.flush()

    # thumbnail
    upload_gallery_thumbnail(img, item)
