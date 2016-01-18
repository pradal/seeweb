from pyramid.view import view_config

from seeweb.models import DBSession

from .tools import tabs, view_init


@view_config(route_name='project_view_source',
             renderer='templates/project/view_source.jinja2')
def index(request):
    session = DBSession()
    project, allow_edit = view_init(request, session)

    return {"project": project,
            "tabs": tabs,
            "tab": 'source',
            "allow_edit": allow_edit,
            "sections": []}
