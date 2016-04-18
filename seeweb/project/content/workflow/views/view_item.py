import json
from openalea.wlformat.convert import svg
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.content_item import ContentItem
from seeweb.views.project.commons import content_init

from seeweb.project.content.alias.commons import resolve_target


@view_config(route_name='project_content_workflow_view_item',
             renderer='../templates/view_item.jinja2')
def view(request):
    session = DBSession()
    project, workflow, workflow_def, view_params = content_init(request, session)

    store = {}
    for node_def in workflow_def['nodes']:
        nid = node_def['id']
        wnode = ContentItem.get(session, nid)
        if wnode is None:
            pass
        elif wnode.category == "alias":
            wnode = resolve_target(session, wnode)
            store[nid] = wnode.load_definition()
            store[nid]['url'] = request.route_url('project_content_alias_view_item', pid=wnode.project, cid=nid)
        else:
            store[nid] = wnode.load_definition()
            store[nid]['url'] = request.route_url('project_content_workflow_node_view_item', pid=wnode.project, cid=nid)

    for nid, node in store.items():
        for port in node['inputs'] + node['outputs']:
            iid = port['interface']
            iface = ContentItem.get(session, iid)
            if iface is None:
                pass
            else:
                store[iid] = iface.load_definition()
                store[iid]['url'] = request.route_url('project_content_interface_view_item', pid=iface.project, cid=iid)

    txt, viewbox = svg.export_workflow(workflow_def, store, (800, 600))
    view_params['svg_repr'] = txt
    view_params['svg_viewbox'] = json.dumps(viewbox)

    return view_params
