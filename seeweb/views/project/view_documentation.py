from pyramid.view import view_config
from urlparse import urlparse

from .tools import view_init


@view_config(route_name='project_view_documentation', renderer='templates/project/view_documentation.jinja2')
def index(request):
    project, allow_edit = view_init(request)
    if project is None:
        return allow_edit

    doc_host = ""
    if len(project.doc_url) > 0:
        url = urlparse(project.doc_url)
        doc_host = url.hostname

    if len(doc_host) == 0:
        doc_host = "doc host"

    return {"project": project,
            "tab": 'documentation',
            "allow_edit": allow_edit,
            "sections": [],
            "doc_host": doc_host}
