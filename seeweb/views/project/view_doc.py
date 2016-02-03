from jinja2 import Markup
from pyramid.view import view_config
from urlparse import urlsplit

from seeweb.models import DBSession

from .commons import view_init


@view_config(route_name='project_view_doc',
             renderer='templates/project/view_doc.jinja2')
def index(request):
    session = DBSession()
    project, view_params = view_init(request, session, 'doc')

    hostname = ""
    if len(project.doc_url) > 0:
        url = urlsplit(project.doc_url)
        hostname = url.hostname

    if hostname is None or len(hostname) == 0:
        hostname = "doc hostname"

    view_params["hostname"] = hostname
    view_params["doc"] = Markup(project.doc)

    return view_params
