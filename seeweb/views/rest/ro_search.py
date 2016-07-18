from importlib import import_module
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.auth import Role
from seeweb.models.research_object import ResearchObject
from seeweb.models.ro_search import search


@view_config(route_name='ro_rest_search', renderer='json')
def view(request):
    session = DBSession()
    user = request.unauthenticated_userid

    if 'uid' in request.GET:
        # search a RO with a specific id
        uid = request.GET['uid']
        ro = ResearchObject.get(session, uid)
        if ro is None:
            return {}
        else:
            # check credentials
            role = ro.access_role(session, user)
            if role == Role.denied:
                return {}
            else:
                return ro.repr_json(full=True)
    else:
        # try to dispatch by type
        if 'type' in request.GET:
            ro_type = request.GET['type']
            mod = import_module("seeweb.ro.%s.search" % ro_type)
            res = mod.search(session, request.GET)
        else:
            res = search(session, request.GET)

        ros = [ResearchObject.get(session, uid) for uid in res]
        return [ro.id for ro in ros
                if ro.access_role(session, user) != Role.denied]
