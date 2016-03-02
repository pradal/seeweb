from nbconvert import HTMLExporter
import nbformat
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.views.project.commons import content_init


@view_config(route_name='project_content_notebook_view_item',
             renderer='../templates/view_item.jinja2')
def view(request):
    session = DBSession()
    project, notebook, nbdef, view_params = content_init(request, session)

    if nbdef is None:
        view_params["notebook_body"] = "<p>No associated notebook</p>"
    else:
        nbdef = nbformat.reads(notebook.definition, 4)
        html_exporter = HTMLExporter()
        html_exporter.template_file = 'basic'
        (body, resources) = html_exporter.from_notebook_node(nbdef)
        view_params["notebook_body"] = body

    return view_params
