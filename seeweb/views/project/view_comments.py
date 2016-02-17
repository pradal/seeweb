from pyramid.view import view_config

from seeweb.models import DBSession

from .commons import view_init


@view_config(route_name='project_view_comments',
             renderer='templates/project/view_comments.jinja2')
def view(request):
    session = DBSession()
    request.session['last'] = request.current_route_url()

    project, view_params = view_init(request, session, 'comments')
    if request.unauthenticated_userid is not None:
        view_params["sections"] = ['edit comment']

    view_params["comments"] = project.fetch_comments(session)

    return view_params
