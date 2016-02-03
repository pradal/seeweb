from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.project.documentation import host_doc_url, recognized_hosts

from .commons import edit_common, edit_init, fetch_documentation


@view_config(route_name='project_edit_doc',
             renderer='templates/project/edit_doc.jinja2')
def view(request):
    session = DBSession()
    project, view_params = edit_init(request, session, 'doc')

    if 'default' in request.params:
        # reload default values for this user
        # actually already done
        pass
    elif 'update' in request.params:
        edit_common(request, session, project)

        # edit project url
        doc_url = str(request.params["doc_url"])
        if len(doc_url) > 0 and doc_url != project.doc_url:
            # do some checks
            project.doc_url = doc_url

        if 'documentation' in request.params:
            # sanitize
            project.doc = request.params['documentation']
    elif "fetch_doc" in request.params:
        doc = fetch_documentation(project.doc_url, project.id)
        if doc is None:
            request.session.flash("Unable to fetch documentation", 'warning')
        else:
            project.doc = doc

    for host in recognized_hosts:
        if host in request.params:
            project.doc_url = host_doc_url(project, host)

    view_params["doc_hosts"] = list(recognized_hosts)

    return view_params
