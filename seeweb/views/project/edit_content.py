from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.project.content.explore import explore_sources
from seeweb.project.explore_sources import fetch_dependencies
from seeweb.project.source import (fetch_sources,
                                   host_src_url,
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
            project.clear_dependencies(session)
            for name, ver in fetch_dependencies(project.id):
                project.add_dependency(session, name, ver)

            explore_sources(session, project)

            loc = request.route_url('project_view_content', pid=project.id)
            return HTTPFound(location=loc)
        else:
            request.session.flash("Unable to fetch sources", 'warning')
    elif 'update' in request.params:
        if "src_url" in request.params:
            project.src_url = request.params['src_url']

    for host in recognized_hosts:
        if host in request.params:
            project.src_url = host_src_url(project, host)

    if len(project.src_url) > 0:
        hostname = parse_hostname(project.src_url)
    else:
        hostname = ""

    view_params["current_hostname"] = hostname

    view_params["src_hosts"] = recognized_hosts

    return view_params
