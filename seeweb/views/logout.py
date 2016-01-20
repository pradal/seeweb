from pyramid.httpexceptions import HTTPFound
from pyramid.security import forget
from pyramid.view import view_config


@view_config(route_name='user_logout')
def index(request):
    request.session.flash("User %s logged out" % request.unauthenticated_userid,
                          'success')

    headers = forget(request)
    return HTTPFound(location=request.route_url('home'),
                     headers=headers)
