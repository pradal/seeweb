from seeweb.ro.workflow_prov.models.ro_workflow_prov import ROWorkflowProv


def search(session, params):
    """Perform a query for ROWorkflowNodes objects

    Args:
        session (DBSession):
        params (dict): extra parameters for search

    Returns:
        (list of str): list of ids of ROContainers matching query
    """
    if 'name' in params:
        # search all RO whose name is equal to the one given
        name = params['name']
        query = session.query(ROWorkflowProv.id)
        query = query.filter(ROWorkflowProv.name == name)
        return [uid for uid, in query.all()]
    else:
        return []
