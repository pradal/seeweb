from seeweb.ro.interface.models.ro_interface import ROInterface


def search(session, params):
    """Perform a query for ROInterface objects

    Args:
        session (DBSession):
        params (dict): extra parameters for search

    Returns:
        (list of str): list of ids of ROContainers matching query
    """
    if 'name' in params:
        # search all ROInterfaces with given title
        name = params['name']
        query = session.query(ROInterface.id)
        query = query.filter(ROInterface.name == name)
        return [uid for uid, in query.all()]
    else:
        return []
