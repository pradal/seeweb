from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.model_access import get_project, get_project_content
from seeweb.project.source import parse_vcs, parse_hostname
from seeweb.project.explore_sources import find_all

from .commons import view_init


@view_config(route_name='project_view_source',
             renderer='templates/project/view_source.jinja2')
def view(request):
    session = DBSession()
    project, view_params = view_init(request, session, 'source')

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
    src_items = find_all(project.id)
    view_params.update(src_items)

    cnt = get_project_content(session, project.id)
    if cnt is not None:
        nbs = []
        for nb in cnt.notebooks:
            nbs.append(("path", nb.name))

        view_params['notebooks'] = nbs

    view_params["sections"] = src_items.keys()

    return view_params
