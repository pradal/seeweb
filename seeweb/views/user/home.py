from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.user import User


@view_config(route_name='user_home', renderer='templates/user/home.jinja2')
def index(request):
    session = DBSession()
    query = session.query(User)
    query = query.filter(User.email.like(request.session["userid"]))
    user = query.all()[0]
    return {"user": user}
