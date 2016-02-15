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
    view_params["wdef"] = workflow.load_definition()

    return view_params
