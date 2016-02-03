from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.project.source import host_src_url, recognized_hosts

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
    elif 'update' in request.params:
        edit_common(request, session, project)
        if "src_url" in request.params:
            project.src_url = request.params['src_url']

    for host in recognized_hosts:
        if host in request.params:
            project.doc_url = host_src_url(project, host)

    view_params["src_hosts"] = list(recognized_hosts)

    return view_params
