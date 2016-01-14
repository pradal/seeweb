from docutils.core import publish_parts
from jinja2 import Markup
from pyramid.view import view_config

from .tools import view_init


@view_config(route_name='user_view_home_default', renderer='templates/user/view_home.jinja2')
@view_config(route_name='user_view_home', renderer='templates/user/view_home.jinja2')
def index(request):
    user, current_uid, allow_edit = view_init(request)

    if user.description == "":
        description = ""
    else:
        html = publish_parts(user.description, writer_name='html')['html_body']
        description = Markup(html)

    return {"user": user,
            "tab": 'home',
            "allow_edit": allow_edit,
            "description": description}
