from dateutil.parser import parse
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.ro.explore import register


@view_config(route_name='ro_rest_register', renderer='json')
def view(request):
    session = DBSession()

    # gather data
    ro_type = request.params["ro_type"]

    data = dict(request.params)
    if "created" in data:
        data["created"] = parse(data["created"])

    # create RO
    ro = register(session, ro_type, data)

    return ro.id
