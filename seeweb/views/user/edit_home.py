from pyramid.view import view_config

from seeweb.avatar import load_image, upload_user_avatar
from seeweb.models import DBSession

from .commons import edit_init


@view_config(route_name='user_edit_home',
             renderer='templates/user/edit_home.jinja2')
def view(request):
    session = DBSession()
    user, view_params = edit_init(request, session, 'home')

    if 'update' in request.params:
        if 'description' in request.params:
            user.store_description(request.params['description'])
    elif 'submit_avatar' in request.params:
        field_storage = request.params['avatar']
        if field_storage == "":
            request.session.flash("Select an image first", 'warning')
        else:
            try:
                img = load_image(field_storage)
                upload_user_avatar(img, user)
                request.session.flash("Avatar submitted", 'success')
            except IOError:
                request.session.flash("Unable to read image", 'warning')
    else:
        pass

    return view_params
