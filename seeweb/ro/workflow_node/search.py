from seeweb.ro.workflow_node.models.ro_workflow_node import ROWorkflowNode


def search(session, params):
    """Perform a query for ROWorkflowNodes objects

    Args:
        session (DBSession):
        params (dict): extra parameters for search

    Returns:
        (list of str): list of ids of ROContainers matching query
    """
    if 'name' in params:
        # search all RO whose title starts with something similar
        name = params['name']
        query = session.query(ROWorkflowNode.id)
        query = query.filter(ROWorkflowNode.name == name)
        return [uid for uid, in query.all()]
    else:
        return []
