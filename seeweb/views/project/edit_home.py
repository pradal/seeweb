from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.views.tools import upload_avatar

from .tools import edit_common, edit_init


@view_config(route_name='project_edit_home',
             renderer='templates/project/edit_home.jinja2')
def view(request):
    session = DBSession()
    project, view_params = edit_init(request, session, 'home')

    if 'default' in request.params:
        # reload default values for this user
        # actually already done
        pass
    elif 'update' in request.params:
        edit_common(request, session, project)

        if 'description' in request.params:
            # sanitize
            project.description = request.params['description']
    elif 'submit_avatar' in request.params:
        field_storage = request.params['avatar']
        if field_storage == "":
            request.session.flash("Select an image first", 'warning')
        else:
            pth = upload_avatar(field_storage,
                                item=project,
                                item_type='project')
            if pth is None:
                request.session.flash("Unable to read image", 'warning')
            else:
                request.session.flash("Avatar submitted", 'success')
    else:
        pass

    return view_params
