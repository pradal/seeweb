from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.model_access import get_workflow_node

from .commons import init_min


@view_config(route_name='project_view_workflow_node',
             renderer='templates/project/content/workflow_node.jinja2')
def view(request):
    session = DBSession()
    project, role, view_params = init_min(request, session)

    nid = request.matchdict['nid']
    node = get_workflow_node(session, nid)
    if node is None:
        loc = request.route_url('project_view_content', pid=project.id)
        return HTTPFound(location=loc)

    view_params["node"] = node

    ndef = node.load_definition()
    view_params["ndef"] = ndef

    return view_params
