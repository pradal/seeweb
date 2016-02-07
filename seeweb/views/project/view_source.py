from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.model_access import get_project, get_user
# from seeweb.playground.workspace import has_workspace
from seeweb.project.source import has_source, parse_vcs, parse_hostname
from seeweb.project.explore_sources import (find_executables,
                                            find_notebooks,
                                            find_workflow_nodes)

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
    for name in ["notebooks", "executables", "nodes"]:
        view_params[name] = []

    if has_source(project.id):
        view_params["notebooks"] = find_notebooks(project.id)
        view_params["executables"] = find_executables(project.id)
        view_params["nodes"] = find_workflow_nodes(project.id)

    playground = False
    # user = get_user(session, view_params["current_uid"])
    # view_params["user"] = user
    # if user is not None and project in user.installed:
    #     if has_workspace(user.id):
    #         playground = True

    view_params["playground"] = playground

    view_params["sections"] = ["dependencies",
                               "notebooks",
                               "executables",
                               "nodes"]

    return view_params
