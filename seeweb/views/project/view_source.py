from pyramid.view import view_config
from urlparse import urlsplit

from seeweb.models import DBSession

from .tools import tabs, view_init


@view_config(route_name='project_view_source',
             renderer='templates/project/view_source.jinja2')
def index(request):
    session = DBSession()
    project, allow_edit = view_init(request, session)

    hostname = ""
    if len(project.src_url) > 0:
        url = urlsplit(project.src_url)
        hostname = url.hostname

    if hostname is None or len(hostname) == 0:
        hostname = "src hostname"

    return {"project": project,
            "tabs": tabs,
            "tab": 'source',
            "allow_edit": allow_edit,
            "sections": [],
            "hostname": hostname}
