from pyramid.view import view_config

from .tools import view_init


@view_config(route_name='project_view_source', renderer='templates/project/view_source.jinja2')
def index(request):
    project, allow_edit = view_init(request)
    if project is None:
        return allow_edit

    return {"project": project,
            "tab": 'source',
            "allow_edit": allow_edit,
            "sections": []}
