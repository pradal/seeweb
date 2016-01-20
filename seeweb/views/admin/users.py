from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.user import User


@view_config(route_name='admin_users',
             renderer='templates/admin/users.jinja2',
             permission='admin')
def view(request):
    session = DBSession()
    query = session.query(User)
    if 'query' in request.params and "all" not in request.params:
        search_pattern = "%s%%" % request.params['query']
        query = query.filter(User.id.like(search_pattern))
    else:
        search_pattern = ""

    return {'users': query.all(),
            'search_pattern': search_pattern}
