from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.auth import Role
from seeweb.models.research_object import ResearchObject


@view_config(route_name='ro_list',
             renderer='templates/ro/listing.jinja2')
def view(request):
    session = DBSession()
    query = session.query(ResearchObject)
    if "type" in request.params:
        query = query.filter(ResearchObject.type == request.params["type"])

    query = query.order_by(ResearchObject.id)

    ros = []
    for ro in query.all():
        role = ro.access_role(session, request.unauthenticated_userid)
        if role is None:
            print "\n"*10, ro.id, None, "\n"*10
        elif role != Role.denied:
            ros.append((Role.to_str(role), ro))

    return {'ros': ros}
