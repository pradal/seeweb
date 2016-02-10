from pyramid.view import view_config


@view_config(route_name='documentation',
             renderer='templates/documentation.jinja2')
def view(request):
    del request
    return {}
