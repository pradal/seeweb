import json
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.content_item import ContentItem
from seeweb.views.project.commons import content_init


@view_config(route_name='project_content_workflow_node_view_item',
             renderer='../templates/view_item.jinja2')
def view(request):
    session = DBSession()
    project, node, node_def, view_params = content_init(request, session)

    idef = {}
    for port in node_def['inputs'] + node_def['outputs']:
        iid = port['interface']
        iface = ContentItem.get(session, iid)
        print "iface", iid, iface, "\n" * 10
        if iface is None:
            idef[iid] = None
        else:
            idef[iid] = iface.load_definition()
            idef[iid]['url'] = request.route_url('project_content_interface_view_item', pid=iface.project, cid=iid)

    view_params["interfaces"] = json.dumps(idef).replace("'", "\\'")

    return view_params
