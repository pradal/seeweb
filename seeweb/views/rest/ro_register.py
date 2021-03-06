from dateutil.parser import parse
import json
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.ro.explore import register, register_data


@view_config(route_name='ro_rest_register', renderer='json')
def view(request):
    session = DBSession()

    ro_def = json.loads(request.params["ro_def"])

    ro_def["owner"] = request.unauthenticated_userid

    if "created" in ro_def:
        ro_def["created"] = parse(ro_def["created"])

    if 'ro_type' in request.params:
        # create RO
        try:
            ro = register(session, request.params["ro_type"], ro_def)
            status = "success"
            msg = ""
            res = ro.id
        except KeyError as e:
            status = "KeyError"
            msg = e.message
            res = None
        except UserWarning as e:
            status = "UserWarning"
            msg = e.message
            res = None
    elif 'interface' in request.params:
        # create ROData
        try:
            ro_def['interface'] = request.params["interface"]
            ro = register_data(session, ro_def)
            status = "success"
            msg = ""
            res = ro.id
        except KeyError as e:
            status = "KeyError"
            msg = e.message
            res = None
        except UserWarning as e:
            status = "UserWarning"
            msg = e.message
            res = None
    else:
        status = "UnsufficientInformation"
        msg = "Unable to create RO with so few info"
        res = None

    ans = dict(status=status, msg=msg, res=res)
    return ans
