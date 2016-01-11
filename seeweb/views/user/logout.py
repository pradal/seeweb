from pyramid.view import view_config

from seeweb.views.tools import get_current_uid, set_current_uid


@view_config(route_name='user_logout', renderer='templates/user/logout.jinja2')
def index(request):
    request.session.flash("User %s logged out" % get_current_uid(request),
                          'success')

    set_current_uid(request, None)

    return {}
