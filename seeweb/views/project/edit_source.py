from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession

from .tools import edit_common, edit_init, tabs


@view_config(route_name='project_edit_source',
             renderer='templates/project/edit_source.jinja2')
def view(request):
    session = DBSession()
    project, allow_edit = edit_init(request, session)

    if 'back' in request.params:
        request.session.flash("Edition cancelled", 'success')
        return HTTPFound(location=request.route_url('project_view_source',
                                                    pid=project.id))

    if 'default' in request.params:
        # reload default values for this user
        # actually already done
        pass
    elif 'update' in request.params:
        edit_common(request, session, project)
    elif "github" in request.params:
        project.src_url = "https://github.com/%s/%s" % (project.owner,
                                                        project.id)
    elif "gforge" in request.params:
        project.src_url = "https://gforge.inria.fr/projects/%s" % project.id
    else:
        pass

    src_hosts = ["github", "gforge"]

    return {"project": project,
            "tabs": tabs,
            "tab": 'source',
            "src_hosts": src_hosts}
