from seeweb.ro.workflow_node.models.ro_workflow_node import ROWorkflowNode


def search(session, params):
    """Perform a query for ROWorkflowNodes objects

    Args:
        session (DBSession):
        params (dict): extra parameters for search

    Returns:
        (list of str): list of ids of ROContainers matching query
    """
    if 'title' in params:
        # search all RO whose title starts with something similar
        title = params['title']
        query = session.query(ROWorkflowNode.id)
        query = query.filter(ROWorkflowNode.title.like("%s%%" % title))
        return [uid for uid, in query.all()]
    else:
        return []
