from pyramid.view import view_config


@view_config(route_name='user_logout', renderer='templates/user/logout.jinja2')
def index(request):
    request.session.flash("User %s logged out" % request.session["userid"],
                          'success')

    request.session["userid"] = None

    return {}
