from pyramid.view import view_config

from seeweb.models import DBSession

from.commons import view_init


@view_config(route_name='home', renderer='templates/home.jinja2')
def view(request):
    session = DBSession()
    view_params = view_init(request, session)

    return view_params
