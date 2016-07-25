from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.auth import Role
from seeweb.models.research_object import ResearchObject


@view_config(route_name='ro_list',
             renderer='templates/ro/listing.jinja2')
def view(request):
    allow_edit = request.unauthenticated_userid is not None

    session = DBSession()
    query = session.query(ResearchObject)
    if "type" in request.params:
        query = query.filter(ResearchObject.type == request.params["type"])

    query = query.order_by(ResearchObject.name)

    res = query.all()
    if "toplevel" in request.params:
        res = [ro for ro in res if ro.is_lonely()]

    ros = []
    for ro in res:
        role = ro.access_role(session, request.unauthenticated_userid)
        if role is None:
            print "\n"*10, ro.id, None, "\n"*10
        elif role != Role.denied:
            ros.append((Role.to_str(role), ro))

    return {'allow_edit': allow_edit, 'ros': ros}
