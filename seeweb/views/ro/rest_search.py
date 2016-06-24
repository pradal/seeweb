from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.research_object import ResearchObject


@view_config(route_name='ro_rest_search', renderer='json')
def view(request):
    session = DBSession()

    print "REST\n" * 10
    print "match", request.matchdict.keys()
    print "GET", request.GET.keys()

    uid = request.GET['uid']
    ro = ResearchObject.get(session, uid)
    if ro is None:
        return {}
    else:
        # check credentials
        pass

        return ro.repr_json()
