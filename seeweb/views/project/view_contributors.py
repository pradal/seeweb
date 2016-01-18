from pyramid.view import view_config

from seeweb.models import DBSession

from .tools import tabs, view_init


@view_config(route_name='project_view_contributors',
             renderer='templates/project/view_contributors.jinja2')
def index(request):
    session = DBSession()
    project, allow_edit = view_init(request, session)

    return {"project": project,
            "tabs": tabs,
            "tab": 'contributors',
            "allow_edit": allow_edit,
            "sections": []}
