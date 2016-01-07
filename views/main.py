from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/index.jinja2')
def index(request):
    # del request
    return {'project': 'seeweb'}
