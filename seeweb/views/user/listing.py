from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.user import User


@view_config(route_name='user_list',
             renderer='templates/user/listing.jinja2')
def view(request):
    session = DBSession()
    query = session.query(User)

    search_pattern = request.params.get("main_search", "")
    if search_pattern != "":
        query = query.filter(User.id.like("%s%%" % search_pattern))

    query = query.order_by(User.id)
    users = query.all()

    return {'users': users,
            'search_pattern': search_pattern}
