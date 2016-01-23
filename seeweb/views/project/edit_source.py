from pyramid.view import view_config

from seeweb.models import DBSession

from .tools import edit_common, edit_init


@view_config(route_name='project_edit_source',
             renderer='templates/project/edit_source.jinja2')
def view(request):
    session = DBSession()
    project, view_params = edit_init(request, session, 'source')

    if 'default' in request.params:
        # reload default values for this user
        # actually already done
        pass
    elif 'update' in request.params:
        edit_common(request, session, project)
        if "src_url" in request.params:
            project.src_url = request.params['src_url']
    elif "github" in request.params:
        project.src_url = "https://github.com/%s/%s" % (project.owner,
                                                        project.id)
    elif "gforge" in request.params:
        project.src_url = "https://gforge.inria.fr/projects/%s" % project.id
    else:
        pass

    view_params["src_hosts"] = ["github", "gforge"]

    return view_params
