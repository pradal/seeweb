from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.project.source import (fetch_sources,
                                   host_src_url,
                                   parse_vcs,
                                   parse_hostname,
                                   recognized_hosts)

from .commons import edit_common, edit_init


@view_config(route_name='project_edit_source',
             renderer='templates/project/edit_source.jinja2')
def view(request):
    session = DBSession()
    project, view_params = edit_init(request, session, 'source')

    if 'default' in request.params:
        # reload default values for this user
        # actually already done
        pass
    elif "submit_local" in request.params:
        field_storage = request.params["local_file"]
        project.src_url = field_storage.filename
    elif "confirm_fetch" in request.params:
        if fetch_sources(project):
            loc = request.route_url('project_view_source', pid=project.id)
            return HTTPFound(location=loc)
        else:
            request.session.flash("Unable to fetch sources", 'warning')
    elif 'update' in request.params:
        edit_common(request, session, project)
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
