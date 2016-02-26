import nbformat
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.views.project.commons import content_init


@view_config(route_name='project_content_notebook_view_item',
             renderer='../templates/view_item.jinja2')
def view(request):
    session = DBSession()
    project, notebook, nbdef, view_params = content_init(request, session)

    notebook_cells = []
    if nbdef is not None:
        nbdef = nbformat.convert(nbformat.from_dict(nbdef), 4)
        notebook_cells.extend(nbdef.cells)
        # # nbdef = nbformat.reads(notebook.definition, 4)
        #
        # # if 'cells' not in nbdef:  # TODO workaround
        # #     nbdef = nbdef['worksheets'][0]
        #
        # for cell in nbdef.cells:
        #     src = [v.strip() for v in cell.get('source', cell.get("input"))]
        #     res = []
        #     for out in cell.outputs:
        #         if out.output_type == "stream":
        #             res.append(('stream', out.text))
        #         elif out.output_type == "error":
        #             txt = [out.ename, out.evalue] + out.traceback
        #             res.append(('error', txt))
        #         elif out.output_type == "execute_result":
        #             for mime_type, data in out.data.items():
        #                 if mime_type == "text/plain":
        #                     res.append(("execute_result", data))
        #         elif out.output_type == "display_data":
        #             for mime_type, data in out.data.items():
        #                 if mime_type == "image/png":
        #                     res.append(("display_data", data))
        #
        #     notebook_cells.append((cell.source, res))

    view_params["notebook_cells"] = notebook_cells

    return view_params
