from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.avatar import load_image, upload_ro_avatar
from seeweb.models import DBSession

from .commons import edit_init


@view_config(route_name='ro_edit_home',
             renderer='templates/ro/edit_home.jinja2')
def view(request):
    session = DBSession()
    ro, view_params = edit_init(request, session, 'home')

    if 'update' in request.params:
        if 'description' in request.params:
            ro.store_description(request.params['description'])
    elif 'submit_avatar' in request.params:
        field_storage = request.params['avatar']
        if field_storage == "":
            request.session.flash("Select an image first", 'warning')
        else:
            try:
                img = load_image(field_storage)
                upload_ro_avatar(img, ro)
                request.session.flash("Avatar submitted", 'success')
                loc = request.route_url('ro_view_home', uid=ro.id)
                return HTTPFound(location=loc)
            except IOError:
                request.session.flash("Unable to read image", 'warning')
    else:
        pass

    return view_params
