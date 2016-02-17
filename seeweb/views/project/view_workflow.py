import json
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.project_content.workflow import Workflow
from seeweb.models.project_content.workflow_node import WorkflowNode

from .commons import init_min


@view_config(route_name='project_view_workflow',
             renderer='templates/project/content/workflow.jinja2')
def view(request):
    session = DBSession()
    project, role, view_params = init_min(request, session)

    wid = request.matchdict['wid']
    workflow = Workflow.get(session, wid)
    if workflow is None:
        loc = request.route_url('project_view_content', pid=project.id)
        return HTTPFound(location=loc)

    view_params["workflow"] = workflow

    wdef = workflow.load_definition()
    view_params["wdef"] = wdef

    ndef = {}
    for node_def in wdef['nodes']:
        nid = node_def['id']
        wnode = WorkflowNode.get(session, nid)
        if wnode is None:
            ndef[nid] = None
        else:
            ndef[nid] = wnode.load_definition()

    print ndef, "\n" * 10

    view_params["nodes"] = ndef
    view_params["ndef"] = json.dumps(ndef)

    # for src, src_port, tgt, tgt_port in wdef['connections']:
    #     print wdef['nodes'][src]['x'], wdef['nodes'][src]['y']
    #     print wdef['nodes'][tgt]['x'], wdef['nodes'][tgt]['y']
    #     print "\n" * 10

    return view_params
