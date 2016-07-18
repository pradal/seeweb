from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.ro_link import ROLink


@view_config(route_name='ro_rest_disconnect', renderer='json')
def view(request):
    session = DBSession()

    # gather data
    src = request.params["source"]
    tgt = request.params["target"]
    link_type = request.params["link_type"]

    # test ownership
    # TODO

    # find link
    query = session.query(ROLink)
    query = query.filter(ROLink.source == src)
    query = query.filter(ROLink.target == tgt)
    query = query.filter(ROLink.type == link_type)
    link, = query.all()

    ROLink.remove(session, link)

    return True
