from jinja2 import Markup
from pyramid.view import view_config

from seeweb.models import DBSession

from seeweb.views.ro.commons import view_init_min


@view_config(route_name='ro_container_view',
             renderer='templates/ro/container_view.jinja2')
def view(request):
    session = DBSession()
    ro, view_params = view_init_min(request, session)

    view_params['description'] = Markup(ro.html_description())

    content = [link.target for link in ro.out_links if link.type == "contains"]
    view_params['content'] = content

    return view_params
