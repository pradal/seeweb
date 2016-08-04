from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.auth import Role
from seeweb.models.research_object import ResearchObject
from seeweb.ro.search import search


@view_config(route_name='ro_rest_search', renderer='json')
def view(request):
    session = DBSession()
    user = request.unauthenticated_userid

    if 'uid' in request.params:
        # search a RO with a specific id
        uid = request.params['uid']
        ro = ResearchObject.get(session, uid)
        if ro is None:
            return None
        else:
            # check credentials
            role = ro.access_role(session, user)
            if role == Role.denied:
                return None
            else:
                return ro.repr_json(full=True)
    else:
        ros = search(session, request.params)
        return [ro.id for ro in ros
                if ro.access_role(session, user) != Role.denied]
