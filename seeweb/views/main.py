from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/index.jinja2')
def index(request):
    if "userid" not in request.session:
        request.session["userid"] = None

    return {}
