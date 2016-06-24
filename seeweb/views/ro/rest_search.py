from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.auth import Role
from seeweb.models.research_object import ResearchObject
from seeweb.models.ro_link import ROLink


@view_config(route_name='ro_rest_search', renderer='json')
def view(request):
    # dispatch by type
    if 'type' in request.GET:
        ro_type = request.GET['type']
        print "ro_type", ro_type, repr(ro_type), "\n" * 10
        loc = request.route_url('ro_%s_rest_search' % ro_type,
                                _query=dict(request.GET))
        return HTTPFound(location=loc)

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
                return ro.repr_json()
    elif 'title' in request.GET:
        # search all RO whose title starts with something similar
        title = request.GET['title']
        query = session.query(ResearchObject)
        query = query.filter(ResearchObject.title.like("%s%%" % title))
        res = list(query.all())
        # check credentials
        res = [ro for ro in res if ro.access_role(session, user) != Role.denied]

        return dict(res=[ro.id for ro in res])
    elif 'contains' in request.GET:
        # search all RO that contains a specific id
        uid = request.GET['contains']
        query = session.query(ROLink).filter(ROLink.target == uid,
                                             ROLink.type == 'contains')
        res = [ResearchObject.get(session, link.source) for link in query.all()]
        # check credentials
        res = [ro for ro in res if ro.access_role(session, user) != Role.denied]

        return dict(res=[ro.id for ro in res])
    elif 'use' in request.GET:
        # search all RO that use a specific id
        uid = request.GET['use']
        query = session.query(ROLink).filter(ROLink.target == uid,
                                             ROLink.type == 'use')
        res = [ResearchObject.get(session, link.source) for link in query.all()]
        # check credentials
        res = [ro for ro in res if ro.access_role(session, user) != Role.denied]

        return dict(res=[ro.id for ro in res])
    else:
        return {}
