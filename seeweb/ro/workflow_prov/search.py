from seeweb.models.ro_link import ROLink


def search(session, params):
    """Perform a query for ROWorkflowNodes objects

    Args:
        session (DBSession):
        params (dict): extra parameters for search

    Returns:
        (list of str): list of ids of ROContainers matching query
    """
    res = None
    if 'consume' in params:
        # search all RO that have consumed the given data
        uid = params['consume']
        query = session.query(ROLink.source)
        query = query.filter(ROLink.target == uid,
                             ROLink.type == 'consume')
        res = {uid for uid, in query.all()}

    if 'produce' in params:
        # search all RO that have been produced by an execution
        uid = params['produce']
        query = session.query(ROLink.target)
        query = query.filter(ROLink.source == uid,
                             ROLink.type == 'produce')
        loc_res = {uid for uid, in query.all()}
        if res is None:
            res = loc_res
        else:
            res &= loc_res

    return res
