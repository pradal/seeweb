from markdown import markdown
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
        notebook_cells = []
    else:
        nbdef = nbformat.convert(nbformat.from_dict(nbdef), 4)
        notebook_cells = nbdef.cells
        for cell in notebook_cells:
            if cell.cell_type == "markdown":
                html = markdown("".join(cell.source))
                cell.source = html

    view_params["notebook_cells"] = notebook_cells

    return view_params
