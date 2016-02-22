from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.views.project.commons import content_init


@view_config(route_name='project_content_notebook_view_item',
             renderer='../templates/view_item.jinja2')
def view(request):
    session = DBSession()
    project, notebook, nbdef, view_params = content_init(request, session)

    nbcells = []
    if 'cells' not in nbdef:  # TODO workaround
        nbdef = nbdef['worksheets'][0]

    for cell in nbdef['cells']:
        src = [v.strip() for v in cell.get('source', cell.get("input"))]
        res = []
        for out in cell['outputs']:
            if out["output_type"] == "stream":
                res.append(('stream', out['text']))
            elif out["output_type"] == "error":
                txt = [out["ename"], out["evalue"]] + out["traceback"]
                res.append(('error', txt))
            elif out['output_type'] == "pyout":
                res.append(("pyout", out["text"]))
            elif out['output_type'] == "display_data":
                res.append(("display_data", out["png"]))

        nbcells.append((src, res))

    view_params["nbcells"] = nbcells

    return view_params
