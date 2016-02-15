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

    wdef = view_params["wdef"]
    for src, src_port, tgt, tgt_port in wdef['connections']:
        print wdef['nodes'][src][1], wdef['nodes'][src][2]
        print wdef['nodes'][tgt][1], wdef['nodes'][tgt][2]
        print "\n" * 10


    return view_params
