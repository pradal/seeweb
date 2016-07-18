from dateutil.parser import parse
import json
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.ro.explore import register


@view_config(route_name='ro_rest_register', renderer='json')
def view(request):
    session = DBSession()

    ro_type = request.params["ro_type"]
    ro_def = json.loads(request.params["ro_def"])

    ro_def["owner"] = request.unauthenticated_userid

    if "created" in ro_def:
        ro_def["created"] = parse(ro_def["created"])

    # create RO
    ro = register(session, ro_type, ro_def)

    return ro.id
