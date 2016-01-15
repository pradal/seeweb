from pyramid.view import view_config

from .tools import fetch_comments, view_init


@view_config(route_name='project_view_comments', renderer='templates/project/view_comments.jinja2')
def index(request):
    request.session['last'] = request.current_route_url()
    project, allow_edit = view_init(request)
    if project is None:
        return allow_edit

    comments = fetch_comments(project.id)

    return {"project": project,
            "tab": 'comments',
            "allow_edit": allow_edit,
            "sections": ['description',
                         'gallery',
                         'comments',
                         'extra info'],
            "comments": comments}
