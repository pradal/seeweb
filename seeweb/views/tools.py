import os
import shutil


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
    file_path = os.path.join('data', pth)

    temp_file_path = file_path + '~'

    input_file.seek(0)
    with open(temp_file_path, 'wb') as output_file:
        shutil.copyfileobj(input_file, output_file)

    os.rename(temp_file_path, file_path)

    return file_path
