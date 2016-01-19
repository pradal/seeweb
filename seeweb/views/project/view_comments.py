from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.access import fetch_comments
from .tools import view_init


@view_config(route_name='project_view_comments',
             renderer='templates/project/view_comments.jinja2')
def index(request):
    session = DBSession()
    request.session['last'] = request.current_route_url()

    project, view_params = view_init(request, session, 'comments')
    if 'current_uid' in view_params:
        view_params["sections"] = ['edit comment']

    view_params["comments"] = fetch_comments(session, project.id)

    return view_params
