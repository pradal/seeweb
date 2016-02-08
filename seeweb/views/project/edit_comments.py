from pyramid.view import view_config

from seeweb.models import DBSession

from .commons import edit_init


@view_config(route_name='project_edit_comments',
             renderer='templates/project/edit_comments.jinja2')
def view(request):
    session = DBSession()
    project, view_params = edit_init(request, session, 'comments')

    return view_params
