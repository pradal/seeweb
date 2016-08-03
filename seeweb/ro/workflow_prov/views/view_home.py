import base64
from itertools import chain
import json
from jinja2 import Markup
from openalea.wlformat.convert import svg
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.ro.interface.models.ro_interface import ROInterface
from seeweb.ro.workflow.models.ro_workflow import ROWorkflow
from seeweb.ro.workflow_node.models.ro_workflow_node import ROWorkflowNode
from seeweb.views.ro.commons import view_init_min


route_name = 'ro_workflow_prov_view_home'
route_url = 'ro_workflow_prov/{uid}/home'


@view_config(route_name=route_name,
             renderer='../templates/view_home.jinja2')
def view(request):
    session = DBSession()
    ro, view_params = view_init_min(request, session)

    view_params['description'] = Markup(ro.html_description())

    prov_def = ro.repr_json(full=True)
    data = {}
    workflow = ROWorkflow.get(session, prov_def['workflow'])
    if workflow is not None:
        store = {}
        workflow_def = workflow.repr_json(full=True)
        for node_def in workflow_def['nodes']:
            nid = node_def['id']
            wnode = ROWorkflowNode.get(session, nid)
            if wnode is None:
                pass
            else:
                store[nid] = wnode.repr_json(full=True)
                store[nid]['url'] = request.route_url('ro_view_home', uid=nid)

        # for nid, node in store.items():
        #     for port in chain(node['inputs'], node['outputs']):
        #         iid = port['interface']
        #         iface = ROInterface.get(session, iid)
        #         if iface is None:
        #             pass
        #         else:
        #             store[iid] = iface.repr_json(full=True)
        #             store[iid]['url'] = request.route_url('ro_view_home',
        #                                                   uid=iid)

        txt, viewbox = svg.export_workflow(workflow_def, store, (800, 600))
        view_params['svg_repr'] = txt
        view_params['svg_viewbox'] = json.dumps(viewbox)

        prov = prov_def
        fmt_data = {}
        for data_obj in prov['data']:
            dtype = data_obj['type']
            if dtype == "ref":  # internally used to reference another RO
                url = request.route_url('ro_view_home', uid=data_obj["value"])
                val = '<p><a href="%s">link to RO</a></p>' % url
            elif dtype == "int":
                val = "<p>%d</p>" % data_obj["value"]
            elif dtype == "str":
                val = "<p>%s</p>" % data_obj["value"]
            elif dtype == "url":
                val = "<p>%s</p>" % data_obj["value"]
            elif dtype == "image":
                img_data = data_obj["value"].replace("\n", "")
                val = '<img src="data:image/png;base64,%s" />' % img_data
            else:
                val = "<p>%s</p>" % json.dumps(data_obj["value"])
            fmt_data[data_obj['id']] = (dtype, val)

        for pexec in prov['executions']:
            nid = pexec['node']
            for port in pexec['inputs']:
                if port['data'] is not None:
                    key = "wkf_node_%d_input_%s" % (nid, port['port'])
                    data[key] = fmt_data[port['data']]

            for port in pexec['outputs']:
                if port['data'] is not None:
                    key = "wkf_node_%d_output_%s" % (nid, port['port'])
                    data[key] = fmt_data[port['data']]

    view_params['wkf_data'] = data

    return view_params
