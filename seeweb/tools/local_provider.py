""" All local provider related functions.

For debug purpose only, raise NotImplementedError in production
"""
import os
from os.path import exists, splitext
from os.path import join as pj
from PIL import Image
from subprocess import call, Popen, PIPE


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


def fetch_sources(src_url, dst):
    """Fetch sources located in src_url
    and copy them into a pid directory in dst.

    Use git clone, check pth is a valid git repo
    """
    cwd = os.getcwd()

    # check dest
    if not exists(dst):
        os.mkdir(dst)

    os.chdir(dst)

    if not exists(".git"):
        call(["git", "init"])

    res = call(["git", "pull", pj(cwd, src_url)])
    # print "res\n" * 10, res

    os.chdir(cwd)

    return True
