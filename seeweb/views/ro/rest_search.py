from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.research_object import ResearchObject
from seeweb.models.ro_link import ROLink


@view_config(route_name='ro_rest_search', renderer='json')
def view(request):
    session = DBSession()

    if 'uid' in request.GET:
        # search a RO with a specific id
        uid = request.GET['uid']
        ro = ResearchObject.get(session, uid)
        if ro is None:
            return {}
        else:
            # check credentials
            pass

            return ro.repr_json()
    elif 'title' in request.GET:
        # search all RO whose title starts with something similar
        title = request.GET['title']
        query = session.query(ResearchObject).filter(ResearchObject.title.like("%s%%" % title))
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
