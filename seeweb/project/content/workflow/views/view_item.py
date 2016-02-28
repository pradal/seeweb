import json
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.content_item import ContentItem
from seeweb.views.project.commons import content_init

from seeweb.project.content.workflow.workflow_draw import draw_workflow


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

    idef = {}
    for nid, node in ndef.items():
        if node is not None:
            for port in node['inputs'] + node['outputs']:
                iid = port['interface']
                iface = ContentItem.get(session, iid)
                if iface is None:
                    idef[iid] = None
                else:
                    idef[iid] = iface.load_definition()
                    idef[iid]['url'] = request.route_url('project_content_interface_view_item', pid=iface.project, cid=iid)

    data = {}
    if workflow.name == "Add integers":
        from seeweb.project.source import source_pth
        from os.path import join
        pth = source_pth(project.id)
        with open(join(pth, "src/sample_project/workflow_add.prov")) as f:
            prov = json.load(f)

        if prov['workflow'] == workflow.id:
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

    svg, viewbox = draw_workflow(workflow_def, ndef, idef, (800, 600))
    view_params['svg_repr'] = svg
    view_params['svg_viewbox'] = json.dumps(viewbox)
    view_params['wkf_data'] = data

    return view_params
