from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.ro_link import ROLink
from seeweb.ro.container.models.ro_container import ROContainer


route_name = 'ro_container_rest_search'
route_url = 'rest/ro_container/search'


@view_config(route_name=route_name, renderer='json')
def view(request):
    session = DBSession()

    if 'title' in request.GET:
        # search all RO whose title starts with something similar
        title = request.GET['title']
        query = session.query(ROContainer).filter(ROContainer.title.like("%s%%" % title))
        res = list(query.all())
        # check credentials

        return dict(res=[ro.id for ro in res])
    elif 'contains' in request.GET:
        # search all RO that contains a specific id
        uid = request.GET['contains']
        query = session.query(ROLink).filter(ROLink.target == uid, ROLink.type == 'contains')
        res = [link.source for link in query.all()]
        # check credentials

        return dict(res=res)
    elif 'use' in request.GET:
        # search all RO that use a specific id
        uid = request.GET['use']
        query = session.query(ROLink).filter(ROLink.target == uid, ROLink.type == 'use')
        res = [link.source for link in query.all()]
        # check credentials

        return dict(res=res)
    else:
        return {}
