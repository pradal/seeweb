from pyramid.view import view_config

from seeweb.models import DBSession

from .commons import view_init


@view_config(route_name='documentation',
             renderer='templates/documentation.jinja2')
def view(request):
    request.session['last'] = request.current_route_url()
    session = DBSession()
    view_params = view_init(request, session)

    return view_params
