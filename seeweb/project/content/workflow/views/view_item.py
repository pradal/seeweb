import json
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.content_item import ContentItem
from seeweb.views.project.commons import content_init


@view_config(route_name='project_content_workflow_view_item',
             renderer='../templates/view_item.jinja2')
def view(request):
    session = DBSession()
    project, workflow, workflow_def, view_params = content_init(request, session)

    ndef = {}
    for node_def in workflow_def['nodes']:
        nid = node_def['id']
        wnode = ContentItem.get(session, nid)
        if wnode is None:
            ndef[nid] = None
        else:
            ndef[nid] = wnode.load_definition()
            ndef[nid]['url'] = request.route_url('project_content_workflow_node_view_item', pid=wnode.project, cid=nid)

    view_params["nodes"] = json.dumps(ndef)

    idef = {}
    for nid, node in ndef.items():
        for port in node['inputs'] + node['outputs']:
            iid = port['interface']
            iface = ContentItem.get(session, iid)
            if iface is None:
                idef[iid] = None
            else:
                idef[iid] = iface.load_definition()
                idef[iid]['url'] = request.route_url('project_content_interface_view_item', pid=iface.project, cid=iid)

    view_params["interfaces"] = json.dumps(idef)

    return view_params
