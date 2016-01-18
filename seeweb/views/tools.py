from docutils.core import publish_parts
import os
from os.path import dirname, exists, join
from PIL import Image
import shutil
import StringIO


def get_current_uid(request):
    """Fetch user_id of currently logged user.

    Return None if no user logged in.
    """
    return request.session.get("userid", None)


def set_current_uid(request, uid):
    """Set the currently logged user
    """
    request.session["userid"] = uid


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


def get_save_pth(pth):
    root = dirname(dirname(__file__))
    return join(root, 'static', pth)


def upload_avatar(field_storage, item, item_type):
    """Upload an image to use as avatar for either
    a team or a single user
    """
    try:
        img = load_image(field_storage)
    except IOError:
        return None

    s = 256
    thumb = Image.new('RGBA', (s, s))
    img.thumbnail((s, s))
    thumb.paste(img, ((s - img.size[0]) / 2, (s - img.size[1]) / 2))

    pth = get_save_pth('avatar/%s/%s.png' % (item_type, item.id))

    if exists(pth):
        os.remove(pth)
    thumb.save(pth)

    thumb.thumbnail((64, 64))

    pth = get_save_pth('avatar/%s/%s_small.png' % (item_type, item.id))

    if exists(pth):
        os.remove(pth)
    thumb.save(pth)

    return pth


def convert_rst_to_html(rst):
    """Convert restructured text into html
    """
    html = publish_parts(rst, writer_name='html')['html_body']
    return html