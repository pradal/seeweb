""" All local provider related functions.

For debug purpose only, raise NotImplementedError in production
"""
import os
from os.path import exists, splitext
from os.path import join as pj
from PIL import Image


def fetch_contributors(pth):
    """ Try to list all contributors for a project
    """
    info = []

    return info


def fetch_readme(pth):
    """Find readme information.
    """
    with open(pj(pth, "readme.rst"), 'r') as f:
        txt = f.read()

    return txt


def fetch_avatar(pth):
    """try to fetch avatar file.
    """
    with open(pj(pth, "avatar.png"), 'rb') as f:
        data = f.read()

    return data


def fetch_gallery_images(pth):
    """Retrieve all images in the gallery
    """
    gal_dir = pj(pth, "gallery")
    if not exists(gal_dir):
        return []

    imgs = []
    for name in os.listdir(gal_dir):
        if splitext(name)[1] == ".png":
            img = Image.open(pj(gal_dir, name))
            imgs.append((name, img))

    return imgs


def fetch_sources(pth, dest):
    """Fetch sources located in pth
    and copy them into dest.

    Use git clone, assume pth is a valid git repo
    """
    raise NotImplementedError
