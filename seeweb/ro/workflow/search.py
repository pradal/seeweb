from seeweb.ro.workflow.models.ro_workflow import ROWorkflow


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
        query = session.query(ROWorkflow.id)
        query = query.filter(ROWorkflow.name.like("%s%%" % name))
        return [uid for uid, in query.all()]
    else:
        return []
