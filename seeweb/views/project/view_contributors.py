from pyramid.view import view_config

from .tools import tabs, view_init


@view_config(route_name='project_view_contributors', renderer='templates/project/view_contributors.jinja2')
def index(request):
    project, allow_edit = view_init(request)
    if project is None:
        return allow_edit

    return {"project": project,
            "tabs": tabs,
            "tab": 'contributors',
            "allow_edit": allow_edit,
            "sections": []}
