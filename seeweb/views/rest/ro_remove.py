import json
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.research_object import ResearchObject


@view_config(route_name='ro_rest_remove', renderer='json')
def view(request):
    session = DBSession()
    uid = request.params["uid"]
    delete_recursive = json.loads(request.params["recursive"])
    ro = ResearchObject.get(session, uid)
    if ro.owner == request.unauthenticated_userid:
        ResearchObject.remove(session, ro, delete_recursive)

    return {}
