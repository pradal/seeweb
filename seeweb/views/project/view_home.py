from jinja2 import Markup
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.access import fetch_comments
from seeweb.views.tools import convert_rst_to_html, fetch_gallery_images

from .tools import view_init


@view_config(route_name='project_view_home_default',
             renderer='templates/project/view_home.jinja2')
@view_config(route_name='project_view_home',
             renderer='templates/project/view_home.jinja2')
def index(request):
    session = DBSession()
    request.session['last'] = request.current_route_url()

    project, view_params = view_init(request, session, 'home')
    view_params["sections"] = ['description',
                               'gallery',
                               'comments',
                               'extra info']

    # description
    if project.description == "":
        view_params["short_description"] = ""
    else:
        html = convert_rst_to_html(project.description)
        view_params["short_description"] = Markup(html)

    # gallery
    view_params["gallery"] = fetch_gallery_images(project.id)

    # comments
    view_params["comments"] = fetch_comments(session, project.id, 2)

    return view_params
