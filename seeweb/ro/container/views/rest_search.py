from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.auth import Role
from seeweb.models.ro_link import ROLink
from seeweb.ro.container.models.ro_container import ROContainer


route_name = 'ro_container_rest_search'
route_url = 'rest/ro_container/search'


@view_config(route_name=route_name, renderer='json')
def view(request):
    session = DBSession()
    user = request.unauthenticated_userid

    if 'title' in request.GET:
        # search all RO whose title starts with something similar
        title = request.GET['title']
        query = session.query(ROContainer)
        query = query.filter(ROContainer.title.like("%s%%" % title))
        res = list(query.all())
        # check credentials
        res = [ro for ro in res if ro.access_role(session, user) != Role.denied]

        return dict(res=[ro.id for ro in res])
    elif 'contains' in request.GET:
        # search all RO that contains a specific id
        uid = request.GET['contains']
        query = session.query(ROLink).filter(ROLink.target == uid,
                                             ROLink.type == 'contains')
        res = [ROContainer.get(session, link.source) for link in query.all()]
        # check credentials
        res = [ro for ro in res if ro.access_role(session, user) != Role.denied]

        return dict(res=[ro.id for ro in res])
    elif 'use' in request.GET:
        # search all RO that use a specific id
        uid = request.GET['use']
        query = session.query(ROLink).filter(ROLink.target == uid,
                                             ROLink.type == 'use')
        res = [ROContainer.get(session, link.source) for link in query.all()]
        # check credentials
        res = [ro for ro in res if ro.access_role(session, user) != Role.denied]

        return dict(res=[ro.id for ro in res])
    else:
        return {}
