import json
from jinja2 import Markup
from openalea.wlformat.convert import svg
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.ro.interface.models.ro_interface import ROInterface
from seeweb.ro.workflow_node.models.ro_workflow_node import ROWorkflowNode
from seeweb.views.ro.commons import view_init_min


route_name = 'ro_workflow_view_home'
route_url = 'ro_workflow/{uid}/home'


@view_config(route_name=route_name,
             renderer='../templates/view_home.jinja2')
def view(request):
    session = DBSession()
    ro, view_params = view_init_min(request, session)

    view_params['description'] = Markup(ro.html_description())

    store = {}
    workflow_def = ro.repr_json(full=True)
    for node_def in workflow_def['nodes']:
        nid = node_def['id']
        wnode = ROWorkflowNode.get(session, nid)
        if wnode is None:
            pass
        # elif wnode.category == "alias":
        #     wnode = resolve_target(session, wnode)
        #     store[nid] = wnode.load_definition()
        #     store[nid]['url'] = request.route_url('project_content_alias_view_item', pid=wnode.project, cid=nid)
        else:
            store[nid] = wnode.repr_json(full=True)
            store[nid]['url'] = request.route_url('ro_view_home', uid=nid)

    for nid, node in store.items():
        for port in node['inputs'] + node['outputs']:
            iid = port['interface']
            iface = ROInterface.get(session, iid)
            if iface is None:
                pass
            else:
                store[iid] = iface.repr_json(full=True)
                store[iid]['url'] = request.route_url('ro_view_home', uid=iid)

    txt, viewbox = svg.export_workflow(workflow_def, store, (800, 600))
    view_params['svg_repr'] = txt
    view_params['svg_viewbox'] = json.dumps(viewbox)

    return view_params
