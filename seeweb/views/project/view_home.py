from jinja2 import Markup
from pyramid.view import view_config

from seeweb.models import DBSession

from .commons import view_init


@view_config(route_name='project_view_home_default',
             renderer='templates/project/view_home.jinja2')
@view_config(route_name='project_view_home',
             renderer='templates/project/view_home.jinja2')
def view(request):
    session = DBSession()
    request.session['last'] = request.current_route_url()

    project, view_params = view_init(request, session, 'home')
    view_params["sections"] = ['description',
                               'gallery',
                               'comments',
                               'extra info']

    # description
    view_params['description'] = Markup(project.html_description())

    # gallery
    view_params["gallery"] = project.fetch_gallery_items(session)

    # comments
    view_params["comments"] = project.fetch_comments(session, 2)

    return view_params
