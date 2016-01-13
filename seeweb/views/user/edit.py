from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.views.tools import get_current_uid

from .tools import get_user


@view_config(route_name='user_edit',
             renderer='templates/user/edit.jinja2')
def view(request):
    uid = request.matchdict['uid']
    current_uid = get_current_uid(request)

    if uid != current_uid:
        request.session.flash("Access to %s edition not granted for you" % uid,
                              'warning')
        return HTTPFound(location=request.route_url('home'))

    if 'cancel' in request.params:
        request.session.flash("Edition cancelled", 'success')
        return HTTPFound(location=request.route_url('user_home', uid=uid))

    user = get_user(request, uid)

    if 'default' in request.params:
        # reload default values for this user
        # actually already done
        pass
    elif 'update' in request.params:
        pass
    else:
        pass

    return {'user': user}
