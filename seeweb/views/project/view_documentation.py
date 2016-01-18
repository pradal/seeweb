from jinja2 import Markup
from pyramid.view import view_config
from urlparse import urlparse

from seeweb.models import DBSession

from .tools import tabs, view_init


@view_config(route_name='project_view_doc',
             renderer='templates/project/view_doc.jinja2')
def index(request):
    session = DBSession()
    project, allow_edit = view_init(request, session)

    doc_host = ""
    if len(project.doc_url) > 0:
        url = urlparse(project.doc_url)
        doc_host = url.hostname

    if doc_host is None or len(doc_host) == 0:
        doc_host = "doc host"

    doc = Markup(project.doc)

    return {"project": project,
            "tabs": tabs,
            "tab": 'doc',
            "allow_edit": allow_edit,
            "sections": [],
            "doc_host": doc_host,
            "doc": doc}
