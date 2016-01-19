from pyramid.view import view_config
from urlparse import urlparse

from seeweb.models import DBSession

from .tools import edit_common, edit_init, fetch_documentation


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

    view_params["doc_hosts"] = ["readthedocs", "pypi"]

    return view_params
