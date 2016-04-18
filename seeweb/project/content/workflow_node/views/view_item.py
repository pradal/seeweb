import json
from openalea.wlformat.convert import svg
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.content_item import ContentItem
from seeweb.views.project.commons import content_init


@view_config(route_name='project_content_workflow_node_view_item',
             renderer='../templates/view_item.jinja2')
def view(request):
    session = DBSession()
    project, node, node_def, view_params = content_init(request, session)

    store = {}
    for port in node_def['inputs'] + node_def['outputs']:
        iid = port['interface']
        iface = ContentItem.get(session, iid)
        if iface is None:
            pass
        else:
            store[iid] = iface.load_definition()
            store[iid]['url'] = request.route_url('project_content_interface_view_item', pid=iface.project, cid=iid)

    txt, viewbox = svg.export_node(node_def, store, (800, 300))
    view_params['svg_repr'] = txt
    view_params['svg_viewbox'] = json.dumps(viewbox)

    return view_params
