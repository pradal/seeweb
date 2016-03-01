from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.user import User
from seeweb.views.project.commons import content_init


@view_config(route_name='project_content_executable_view_item',
             renderer='../templates/view_item.jinja2')
def view(request):
    session = DBSession()
    project, exe, exe_def, view_params = content_init(request, session)

    user = User.get(session, request.unauthenticated_userid)
    if user is None:
        view_params["installed"] = False
    else:
        view_params["installed"] = project.id in (inst.project for inst in user.installed)

    return view_params
