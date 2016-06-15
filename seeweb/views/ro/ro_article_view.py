from jinja2 import Markup
from pyramid.view import view_config

from seeweb.models import DBSession

from seeweb.views.ro.commons import view_init_min


@view_config(route_name='ro_article_view',
             renderer='templates/ro/article_view.jinja2')
def view(request):
    session = DBSession()
    ro, view_params = view_init_min(request, session)

    view_params['description'] = Markup(ro.html_description())

    citations = [link.source for link in ro.in_links if link.type == "use"]
    view_params['citations'] = citations

    return view_params
