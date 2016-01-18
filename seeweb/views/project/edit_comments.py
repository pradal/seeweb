from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession

from .tools import edit_common, edit_init, tabs


@view_config(route_name='project_edit_comments',
             renderer='templates/project/edit_comments.jinja2')
def view(request):
    session = DBSession()
    project, allow_edit = edit_init(request, session)

    if 'back' in request.params:
        request.session.flash("Edition cancelled", 'success')
        loc = request.route_url('project_view_comments', pid=project.id)
        return HTTPFound(location=loc)

    if 'default' in request.params:
        # reload default values for this user
        # actually already done
        pass
    elif 'update' in request.params:
        edit_common(request, session, project)
    else:
        pass

    return {"project": project,
            "tabs": tabs,
            "tab": 'comments'}
