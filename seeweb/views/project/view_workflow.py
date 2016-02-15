from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.model_access import get_workflow

from .commons import init_min


@view_config(route_name='project_view_workflow',
             renderer='templates/project/content/workflow.jinja2')
def view(request):
    session = DBSession()
    project, role, view_params = init_min(request, session)

    wid = request.matchdict['wid']
    workflow = get_workflow(session, wid)

    view_params["workflow"] = workflow

    print "nodes", workflow.nodes, "\n" * 10
    print "links", workflow.links, "\n" * 10
    for link in workflow.links:
        print "link", workflow.nodes[link.source], "\n" * 10

    return view_params
