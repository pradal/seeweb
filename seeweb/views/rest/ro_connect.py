from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.ro_link import ROLink


@view_config(route_name='ro_rest_connect', renderer='json')
def view(request):
    session = DBSession()

    # gather data
    src = request.params["src"]
    tgt = request.params["tgt"]
    link_type = request.params["link_type"]

    # test ownership
    # TODO

    # create link
    link = ROLink.connect(session, src, tgt, link_type)

    return True
