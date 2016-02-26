from pyramid.view import view_config
from sqlalchemy.sql import func

from seeweb.models import DBSession
from seeweb.models.gallery_item import GalleryItem

from.commons import view_init


@view_config(route_name='home', renderer='templates/home.jinja2')
def view(request):
    request.session['last'] = request.current_route_url()
    session = DBSession()
    view_params = view_init(request, session)

    query = session.query(GalleryItem)
    items = query.order_by(func.random()).limit(10).all()

    view_params['items'] = items

    return view_params
