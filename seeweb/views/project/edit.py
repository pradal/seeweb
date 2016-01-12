from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.views.tools import get_current_uid

from .tools import get_project


@view_config(route_name='project_edit',
             renderer='templates/project/edit.jinja2')
def view(request):
    uid = request.matchdict['uid']
    pid = request.matchdict['pid']
    current_uid = get_current_uid(request)

    if 'cancel' in request.params:
        request.session.flash("Edition cancelled", 'success')
        return HTTPFound(location=request.route_url('project_home', uid=uid, pid=pid))

    project = get_project(request, uid, pid)

    if project.owner != current_uid:
        request.session.flash("Access to %s edition not granted for you" % pid,
                              'warning')
        return HTTPFound(location=request.route_url('project_home', uid=uid, pid=pid))

    if 'default' in request.params:
        # reload default values for this user
        # actually already done
        pass
    elif 'update' in request.params:
        # edit project visibility
        public = 'visibility' in request.params
        project.public = public
    else:
        pass

    return {'project': project}
