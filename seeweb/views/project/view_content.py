from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.project_content.content import item_types
from seeweb.model_access import get_project, get_project_content
from seeweb.project.source import parse_vcs, parse_hostname

from .commons import view_init


@view_config(route_name='project_view_content',
             renderer='templates/project/view_content.jinja2')
def view(request):
    session = DBSession()
    project, view_params = view_init(request, session, 'content')

    if len(project.src_url) > 0:
        vcs = parse_vcs(project.src_url)
        hostname = parse_hostname(project.src_url)
    else:
        vcs = ""
        hostname = ""

    view_params["vcs"] = vcs
    view_params["hostname"] = hostname

    # dependencies
    dependencies = []
    for dep in project.dependencies:
        pjt = get_project(session, dep.name)
        if pjt is None:
            dependencies.append((dep.name, "ver: %s" % dep.version, False))
        else:
            dependencies.append((pjt, "ver: %s" % dep.version, True))

    view_params["dependencies"] = dependencies

    # explore sources
    cnt = get_project_content(session, project.id)
    if cnt is not None:
        view_params["sections"] = item_types
        for item_type in item_types:
            view_params[item_type] = list(getattr(cnt, item_type))

    return view_params
