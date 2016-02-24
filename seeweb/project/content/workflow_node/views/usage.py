import json
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.content_item import ContentItem
from seeweb.views.project.commons import content_init_min


def workflow_use(wdef, nid):
    """Check whether the given node id appears in workflow def

    Args:
        wdef: (Workflow)
        nid: (str) node id

    Returns:
        (Bool)
    """
    for node in wdef['nodes']:
        if node['id'] == nid:
            return True

    return False


@view_config(route_name='project_content_workflow_node_usage',
             renderer='../templates/usage.jinja2')
def view(request):
    session = DBSession()
    project, node, node_def, view_params = content_init_min(request, session)

    query = session.query(ContentItem)
    query = query.filter(ContentItem.category == "workflow")
    # query = query.limit(10)

    workflows = []
    for workflow in query.all():
        wdef = workflow.load_definition()
        if workflow_use(wdef, node.id):
            workflows.append(workflow)

    view_params['workflows'] = workflows

    return view_params
