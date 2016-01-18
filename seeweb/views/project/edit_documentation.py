from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from urlparse import urlparse

from seeweb.models import DBSession

from .tools import edit_common, edit_init, fetch_documentation, tabs


@view_config(route_name='project_edit_doc',
             renderer='templates/project/edit_doc.jinja2')
def view(request):
    session = DBSession()
    project, allow_edit = edit_init(request, session)

    if 'back' in request.params:
        request.session.flash("Edition cancelled", 'success')
        return HTTPFound(location=request.route_url('project_view_doc',
                                                    pid=project.id))

    if 'default' in request.params:
        # reload default values for this user
        # actually already done
        pass
    elif 'update' in request.params:
        edit_common(request, session, project)

        # edit project url
        doc_url = request.params["doc_url"]
        if len(doc_url) > 0:
            url = urlparse(doc_url)
            # do some checks
            project.doc_url = str(doc_url)

        if 'documentation' in request.params:
            # sanitize
            project.doc = request.params['documentation']
    elif "fetch_doc" in request.params:
        doc = fetch_documentation(project.doc_url, project.id)
        if doc is None:
            request.session.flash("Unable to fetch documentation", 'warning')
        else:
            project.doc = doc
    elif "readthedocs" in request.params:
        project.doc_url = "https://%s.readthedocs.org/en/latest/" % project.id
    elif "pypi" in request.params:
        project.doc_url = "https://pythonhosted.org/%s" % project.id
    else:
        pass

    doc_hosts = ["readthedocs", "pypi"]

    return {"project": project,
            "tabs": tabs,
            "tab": 'doc',
            "doc_hosts": doc_hosts}
