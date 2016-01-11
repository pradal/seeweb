from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.user import User


@view_config(route_name='project_home', renderer='templates/project/home.jinja2')
def index(request):
    return {}
