from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.research_object import ResearchObject


@view_config(route_name='admin_ros',
             renderer='templates/admin/ros.jinja2',
             permission='admin')
def view(request):
    session = DBSession()
    query = session.query(ResearchObject)

    search_pattern = request.params.get("main_search", "")
    if search_pattern != "":
        query = query.filter(ResearchObject.title.like("%s%%" % search_pattern))

    return {'ros': query.all(),
            'search_pattern': search_pattern}
