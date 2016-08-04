from seeweb.models.ro_link import ROLink


def search(session, params):
    """Perform a query for ROContainer objects

    Args:
        session (DBSession):
        params (dict): extra parameters for search

    Returns:
        (list of str): list of ids of ROContainers matching query
    """
    res = None
    if 'contains' in params:
        uid = params['contains']
        query = session.query(ROLink.source)
        query = query.filter(ROLink.target == uid, ROLink.type == 'contains')
        res = {uid for uid, in query.all()}

    return res
