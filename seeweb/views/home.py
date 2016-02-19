from pyramid.view import view_config
from sqlalchemy.sql import func

from seeweb.models import DBSession
from seeweb.models.content_item import ContentItem

from.commons import view_init


@view_config(route_name='home', renderer='templates/home.jinja2')
def view(request):
    session = DBSession()
    view_params = view_init(request, session)

    query = session.query(ContentItem)
    items = query.order_by(func.random()).limit(5).all()

    view_params['items'] = items

    return view_params
