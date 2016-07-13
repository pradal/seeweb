from seeweb.ro.interface.models.ro_interface import ROInterface


def search(session, params):
    """Perform a query for ROInterface objects

    Args:
        session (DBSession):
        params (dict): extra parameters for search

    Returns:
        (list of str): list of ids of ROContainers matching query
    """
    if 'title' in params:
        # search all ROInterfaces with given title
        title = params['title']
        query = session.query(ROInterface.id)
        query = query.filter(ROInterface.title == title)
        return [uid for uid, in query.all()]
    else:
        return []
