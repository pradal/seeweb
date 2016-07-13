from itertools import chain
import json
from jinja2 import Markup
from openalea.wlformat.convert import svg
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.ro.interface.models.ro_interface import ROInterface
from seeweb.views.ro.commons import view_init_min


route_name = 'ro_workflow_node_view_home'
route_url = 'ro_workflow_node/{uid}/home'


@view_config(route_name=route_name,
             renderer='../templates/view_home.jinja2')
def view(request):
    session = DBSession()
    ro, view_params = view_init_min(request, session)

    view_params['description'] = Markup(ro.html_description())

    store = {}
    node_def = ro.load_definition()
    for port in chain(node_def['inputs'], node_def['outputs']):
        iid = port['interface']
        iface = ROInterface.get(session, iid)
        if iface is None:
            pass
        else:
            store[iid] = iface.load_definition()
            store[iid]['url'] = request.route_url('ro_view_home', uid=iid)

    txt, viewbox = svg.export_node(node_def, store, (800, 300))
    view_params['svg_repr'] = txt
    view_params['svg_viewbox'] = json.dumps(viewbox)

    return view_params
