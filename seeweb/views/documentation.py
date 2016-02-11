from pyramid.view import view_config


@view_config(route_name='documentation',
             renderer='templates/documentation.jinja2')
def view(request):
    request.session['last'] = request.current_route_url()

    return {}
