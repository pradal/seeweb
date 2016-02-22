from jinja2 import Markup
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.project.documentation import parse_hostname

from .commons import view_init


@view_config(route_name='project_view_doc',
             renderer='templates/project/view_doc.jinja2')
def view(request):
    session = DBSession()
    project, view_params = view_init(request, session, 'doc')

    if len(project.doc_url) > 0:
        hostname = parse_hostname(project.doc_url)
    else:
        hostname = ""

    view_params["hostname"] = hostname
    view_params["doc"] = Markup(project.doc)

    return view_params
