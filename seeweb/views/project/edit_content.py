from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.model_edit import (add_dependency,
                               clear_dependencies,
                               clear_project_content,
                               create_executable,
                               create_notebook,
                               create_workflow_node,
                               create_workflow)
from seeweb.project.explore_sources import (fetch_dependencies,
                                            find_executables,
                                            find_notebooks,
                                            find_workflow_nodes,
                                            find_workflows)
from seeweb.project.source import (fetch_sources,
                                   host_src_url,
                                   parse_vcs,
                                   parse_hostname,
                                   recognized_hosts)

from .commons import edit_init


@view_config(route_name='project_edit_content',
             renderer='templates/project/edit_content.jinja2')
def view(request):
    session = DBSession()
    project, view_params = edit_init(request, session, 'content')

    if "submit_local" in request.params:
        field_storage = request.params["local_file"]
        project.src_url = field_storage.filename
    elif "confirm_fetch_src" in request.params:
        if fetch_sources(project):
            clear_dependencies(session, project)
            for name, ver in fetch_dependencies(project.id):
                add_dependency(session, project, name, ver)

            clear_project_content(session, project)
            for executable in find_executables(project.id):
                create_executable(session, project, executable)

            for notebook in find_notebooks(project.id):
                create_notebook(session, project, notebook[1])

            for node in find_workflow_nodes(project.id):
                create_workflow_node(session, project, node)

            for workflow in find_workflows(project.id):
                create_workflow(session, project, workflow)

            loc = request.route_url('project_view_content', pid=project.id)
            return HTTPFound(location=loc)
        else:
            request.session.flash("Unable to fetch sources", 'warning')
    elif 'update' in request.params:
        if "src_url" in request.params:
            project.src_url = request.params['src_url']

    for host in recognized_hosts.keys():
        if host in request.params:
            project.src_url = host_src_url(project, host)

    if len(project.src_url) > 0:
        vcs = parse_vcs(project.src_url)
        hostname = parse_hostname(project.src_url)
    else:
        vcs = ""
        hostname = ""

    view_params["vcs"] = vcs
    view_params["current_hostname"] = hostname

    view_params["src_hosts"] = recognized_hosts.keys()

    return view_params
