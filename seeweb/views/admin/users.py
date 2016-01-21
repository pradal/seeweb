from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.user import User


@view_config(route_name='admin_users',
             renderer='templates/admin/users.jinja2',
             permission='admin')
def view(request):
    session = DBSession()
    query = session.query(User)
    search_pattern = request.params.get("main_search", "")
    if search_pattern != "":
        query = query.filter(User.id.like("%s%%" % search_pattern))

    return {'users': query.all(),
            'search_pattern': search_pattern}
