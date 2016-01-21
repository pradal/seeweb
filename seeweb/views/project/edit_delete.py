from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.access import get_project
from seeweb.models.edit import remove_project


@view_config(route_name='project_edit_delete',
             renderer='templates/project/edit_delete.jinja2')
def view(request):
    session = DBSession()
    pid = request.matchdict['pid']

    project = get_project(session, pid)
    if project is None:
        request.session.flash("Project %s does not exists" % pid, 'warning')
        raise HTTPFound(location=request.route_url('home'))

    current_uid = request.unauthenticated_userid
    if current_uid != project.owner:
        request.session.flash("Delete %s not granted for you" % pid,
                              'warning')
        raise HTTPFound(location=request.route_url('home'))

    if 'cancel' in request.params:
        loc = request.route_url('project_view_home', pid=pid)
        raise HTTPFound(location=loc)

    if 'delete' in request.params:
        if remove_project(session, project):
            request.session.flash("Project %s has been deleted" % pid, 'success')
            loc = request.route_url('user_view_projects', uid=current_uid)
            return HTTPFound(location=loc)
        else:
            request.session.flash("Problem with deletion of " % pid, 'warning')
            loc = request.route_url('user_view_projects', uid=current_uid)
            return HTTPFound(location=loc)

    return {"project": project}
