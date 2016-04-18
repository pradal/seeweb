import json
from openalea.wlformat.convert import svg
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.content_item import ContentItem
from seeweb.project.content.alias.commons import resolve_target
from seeweb.views.project.commons import content_init


@view_config(route_name='project_content_workflow_prov_view_item',
             renderer='../templates/view_item.jinja2')
def view(request):
    session = DBSession()
    project, prov, prov_def, view_params = content_init(request, session)

    data = {}
    workflow = ContentItem.get(session, prov_def['workflow'])
    if workflow is not None:
        workflow_def = workflow.load_definition()
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

        txt, viewbox = svg.export_workflow(workflow_def, store, (800, 600))
        view_params['svg_repr'] = txt
        view_params['svg_viewbox'] = json.dumps(viewbox)

        prov = prov_def
        fmt_data = {}
        for data_obj in prov['data']:
            dtype = data_obj['type']
            if dtype == 'int':
                val = "<p>%d</p>" % data_obj["value"]
            elif dtype == "str":
                val = "<p>%s</p>" % data_obj["value"]
            elif dtype == "url":
                val = "<p>%s</p>" % data_obj["value"]
            elif dtype == "png":
                img_data = data_obj["value"].replace("\n", "")
                val = '<img src="data:image/png;base64,%s" />' % img_data
            else:
                val = "<p>%s</p>" % data_obj["value"]
            fmt_data[data_obj['id']] = (dtype, val)

        for pexec in prov['executions']:
            nid = pexec['node']
            for port in pexec['inputs']:
                key = "wkf_node_%d_input_%s" % (nid, port['port'])
                data[key] = fmt_data[port['data']]

            for port in pexec['outputs']:
                key = "wkf_node_%d_output_%s" % (nid, port['port'])
                data[key] = fmt_data[port['data']]

    view_params['wkf_data'] = data

    return view_params
