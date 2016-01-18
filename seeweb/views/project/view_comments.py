from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.access import fetch_comments
from .tools import tabs, view_init


@view_config(route_name='project_view_comments',
             renderer='templates/project/view_comments.jinja2')
def index(request):
    session = DBSession()
    request.session['last'] = request.current_route_url()
    project, allow_edit = view_init(request, session)

    comments = fetch_comments(session, project.id)

    return {"project": project,
            "tabs": tabs,
            "tab": 'comments',
            "allow_edit": allow_edit,
            "sections": ['description',
                         'gallery',
                         'comments',
                         'extra info'],
            "comments": comments}
