from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.views.tools import upload_avatar

from .tools import edit_common, edit_init, tabs


@view_config(route_name='user_edit_home',
             renderer='templates/user/edit_home.jinja2')
def view(request):
    session = DBSession()
    user, current_uid = edit_init(request, session)

    if 'back' in request.params:
        request.session.flash("Edition cancelled", 'success')
        return HTTPFound(location=request.route_url('user_view_home',
                                                    uid=user.id))

    if 'default' in request.params:
        # reload default values for this user
        # actually already done
        pass
    elif 'update' in request.params:
        edit_common(request, session, user)

        if 'description' in request.params:
            # sanitize
            user.description = request.params['description']
    elif 'submit_avatar' in request.params:
        field_storage = request.params['avatar']
        if field_storage == "":
            request.session.flash("Select an image first", 'warning')
        else:
            pth = upload_avatar(field_storage, item=user, item_type='user')
            if pth is None:
                request.session.flash("Unable to read image", 'warning')
            else:
                request.session.flash("Avatar submitted", 'success')
    else:
        pass

    return {'user': user,
            "tabs": tabs,
            'tab': 'home'}
