from jinja2 import Markup
from os.path import splitext
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.project import Project
from seeweb.project.source import upload_src_file


@view_config(route_name='file_suck',
             renderer='templates/user/file_suck.jinja2')
def view(request):
    session = DBSession()

    if request.unauthenticated_userid is None:
        request.session.flash("Action not authorized for anonymous users",
                              'warning')
        raise HTTPFound(location=request.route_url('home'))

    view_params = {}
    if 'submit_upload' not in request.params:
        return view_params

    field_storage = request.params['upload']
    if field_storage == "":
        request.session.flash("Select a file first", 'warning')
        return view_params

    project_name = splitext(field_storage.filename)[0]

    if "project_name" in request.params:
        project_name = request.params["project_name"]

    pid = project_name.lower().strip()
    if " " in pid:
        request.session.flash("Project names can not contains spaces", 'warning')
        return view_params

    project = Project.get(session, pid)
    if project is not None:
        if project.public:
            project_url = request.route_url('project_view_home',
                                            pid=pid)
            msg = "Project <a href='%s'>'%s'</a> already exists" % (project_url, pid)
            request.session.flash(Markup(msg), 'warning')
        else:
            msg = "Project '%s' already exists (private)" % pid
            request.session.flash(msg, 'warning')

        view_params["project_name"] = pid
        return view_params

    # create project
    project = Project.create(session,
                             request.unauthenticated_userid,
                             pid,
                             public=False)

    # copy sources
    try:
        upload_src_file(field_storage, pid)
        request.session.flash("File submitted", 'success')
    except IOError:
        request.session.flash("Unable to read file", 'warning')

    loc = request.route_url('project_view_home', pid=pid)
    return HTTPFound(location=loc)
