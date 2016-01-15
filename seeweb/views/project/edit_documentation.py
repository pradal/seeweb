from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from .tools import edit_common, edit_init, tabs


@view_config(route_name='project_edit_doc',
             renderer='templates/project/edit_doc.jinja2')
def view(request):
    project, allow_edit = edit_init(request)
    if project is None:
        return allow_edit

    if 'back' in request.params:
        request.session.flash("Edition cancelled", 'success')
        return HTTPFound(location=request.route_url('project_view_doc', pid=project.id))

    if 'default' in request.params:
        # reload default values for this user
        # actually already done
        pass
    elif 'update' in request.params:
        edit_common(request, project)
    else:
        pass

    return {"project": project,
            "tabs": tabs,
            "tab": 'doc'}
