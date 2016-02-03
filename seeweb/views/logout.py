from pyramid.view import view_config

from seeweb.security import log_user_out


@view_config(route_name='user_logout')
def view(request):
    request.session.flash("User %s logged out" % request.unauthenticated_userid,
                          'success')

    return log_user_out(request)
