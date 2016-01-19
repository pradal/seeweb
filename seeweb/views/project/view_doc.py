from jinja2 import Markup
from pyramid.view import view_config
from urlparse import urlsplit

from seeweb.models import DBSession

from .tools import tabs, view_init


@view_config(route_name='project_view_doc',
             renderer='templates/project/view_doc.jinja2')
def index(request):
    session = DBSession()
    project, current_uid, allow_edit = view_init(request, session)

    hostname = ""
    if len(project.doc_url) > 0:
        url = urlsplit(project.doc_url)
        hostname = url.hostname

    if hostname is None or len(hostname) == 0:
        hostname = "doc hostname"

    doc = Markup(project.doc)

    return {"project": project,
            "tabs": tabs,
            "tab": 'doc',
            "allow_edit": allow_edit,
            "sections": [],
            "hostname": hostname,
            "doc": doc}
