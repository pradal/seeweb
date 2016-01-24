from docutils.core import publish_parts
import os
from os.path import dirname, exists, join, splitext
from PIL import Image
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember
import shutil
import StringIO


def avatar_pth(item_type, item_name, small=False):
    """Return a path to avatar.

    Not testing its existence.
    """
    root = dirname(dirname(__file__))
    if small:
        name = "%s_small.png" % item_name
    else:
        name = "%s.png" % item_name

    return join(root, "avatar", item_type, name)


def gallery_pth(pid):
    """Return a path to the gallery associated to a given project.
    """
    root = dirname(dirname(__file__))
    return join(root, "gallery", pid)


def source_pth(pid):
    """Return a path to the source dir associated to a given project.
    """
    root = dirname(dirname(dirname(__file__)))
    return join(root, "data", "sources", pid)


def check_password(session, user, pwd):
    return pwd == user.id


def log_user(request, uid, edit=False):
    """Perform login, assume all credentials are OK
    """
    headers = remember(request, uid)
    if edit:
        loc = request.route_url('user_edit_home', uid=uid)
    else:
        loc = request.route_url('user_view_home', uid=uid)

    return HTTPFound(location=loc, headers=headers)


def store_file(field_storage, pth):
    """Copy data in field_storage to a given location.
    """
    input_file = field_storage.file
    root = dirname(dirname(__file__))
    file_path = join(root, 'static', pth)

    temp_file_path = file_path + '~'

    input_file.seek(0)
    with open(temp_file_path, 'wb') as output_file:
        shutil.copyfileobj(input_file, output_file)

    if exists(file_path):
        os.remove(file_path)

    os.rename(temp_file_path, file_path)

    return file_path


def load_image(field_storage):
    """Generate an image from data in field_storage
    """
    input_file = field_storage.file
    input_file.seek(0)
    img = Image.open(StringIO.StringIO(input_file.read()))

    return img


def clean_avatar(item, item_type):
    pth = avatar_pth(item_type, item.id, small=False)

    if exists(pth):
        os.remove(pth)

    pth = avatar_pth(item_type, item.id, small=True)

    if exists(pth):
        os.remove(pth)


def upload_avatar(img, item, item_type):
    """Upload an image to use as avatar for either
    a team or a single user
    """
    s = 256
    thumb = Image.new('RGBA', (s, s))
    img.thumbnail((s, s))
    thumb.paste(img, ((s - img.size[0]) / 2, (s - img.size[1]) / 2))

    pth = avatar_pth(item_type, item.id, small=False)
    print "pth\n" * 10, pth

    if exists(pth):
        os.remove(pth)
    thumb.save(pth)

    s = 64
    thumb = Image.new('RGBA', (s, s))
    img.thumbnail((s, s))
    thumb.paste(img, ((s - img.size[0]) / 2, (s - img.size[1]) / 2))

    pth = avatar_pth(item_type, item.id, small=True)

    if exists(pth):
        os.remove(pth)
    thumb.save(pth)


def convert_rst_to_html(rst):
    """Convert restructured text into html
    """
    html = publish_parts(rst, writer_name='html')['html_body']
    return html


def fetch_gallery_images(pid):
    """List all available image in gallery associated
    to the given project.
    """
    gal_dir = gallery_pth(pid)
    imgs = []
    if not exists(gal_dir):
        return imgs

    for img_name in os.listdir(gal_dir):
        name, ext = splitext(img_name)
        if ext == ".png" and not name.endswith("_small"):
            imgs.append(name)

    return imgs


def clear_gallery(pid):
    """Remove all images from gallery
    """
    gal_dir = gallery_pth(pid)
    if exists(gal_dir):
        shutil.rmtree(gal_dir)


def add_gallery_image(pid, img, img_name):
    """Save a new image in the gallery of a project
    """
    gal_dir = gallery_pth(pid)
    if not exists(gal_dir):
        os.mkdir(gal_dir)

    img_pth = join(gal_dir, img_name)
    if exists(img_pth):
        os.remove(img_pth)

    img.save(img_pth)

    # thumbnail
    img.thumbnail((256, 256))
    th_name = "%s_small%s" % splitext(img_name)
    th_pth = join(gal_dir, th_name)
    if exists(th_pth):
        os.remove(th_pth)

    img.save(th_pth)
