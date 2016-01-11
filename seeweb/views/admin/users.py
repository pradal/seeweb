from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.user import User


@view_config(route_name='users_admin',
             renderer='templates/admin/users.jinja2')
def view(request):
    session = DBSession()
    query = session.query(User)
    if 'query' in request.params:
        search_pattern = "%s%%" % request.params['query']
        query = query.filter(User.display_name.like(search_pattern))
    else:
        search_pattern = ""

    users = query.all()
    for i, user in enumerate(users):
        if i % 2 == 0:
            user.parity = "even"
        else:
            user.parity = "odd"

    return {'users': users, 'search_pattern': search_pattern}
