"""Set of functions used to manage galleries
"""
import os
from os.path import dirname, exists, join, splitext
from PIL import Image
from shutil import rmtree


def gallery_pth(project):
    """Return the path to the gallery of images associated with a project.

    Warnings: does not test if path exists

    Args:
        project: (Project)

    Returns:
        (str): pth to gallery dir
    """
    root = dirname(__file__)

    return join(root, "data", "gallery", project.id)


def fetch_gallery_images(project):
    """List all available image in gallery associated
    to the given project.

    Args:
        project: (Project)

    Returns:
        (list of str): path to gallery images
    """
    gal_dir = gallery_pth(project)
    imgs = []
    if not exists(gal_dir):
        return imgs

    for img_name in os.listdir(gal_dir):
        name, ext = splitext(img_name)
        if ext == ".png" and not name.endswith("_small"):
            imgs.append(name)

    return imgs


def clear_gallery(project):
    """Remove all images from gallery.

    Args:
        project: (Project)

    Returns:
        (None)
    """
    gal_dir = gallery_pth(project)
    if exists(gal_dir):
        rmtree(gal_dir)


def add_gallery_image(project, img, img_name):
    """Save a new image in the gallery of a project.

    Args:
        project: (Project)
        img: (Image)
        img_name: (str) name to use to store image

    Returns:
        None
    """
    gal_dir = gallery_pth(project)
    if not exists(gal_dir):
        os.mkdir(gal_dir)

    img_pth = join(gal_dir, img_name)
    if exists(img_pth):
        os.remove(img_pth)

    img.save(img_pth)

    # thumbnail
    s = 256
    thumb = Image.new('RGBA', (s, s))
    img.thumbnail((s, s))
    thumb.paste(img, ((s - img.size[0]) / 2, (s - img.size[1]) / 2))

    th_name = "%s_small%s" % splitext(img_name)
    th_pth = join(gal_dir, th_name)
    if exists(th_pth):
        os.remove(th_pth)

    thumb.save(th_pth)
