from seeweb.models.ro_search import search as ro_search
from seeweb.ro.container.models.ro_container import ROContainer


def search(session, params):
    """Perform a query for ROContainer objects

    Args:
        session (DBSession):
        params (dict): extra parameters for search

    Returns:
        (list of str): list of ids of ROContainers matching query
    """
    if 'name' in params:
        # search all RO whose title starts with something similar
        name = params['name']
        query = session.query(ROContainer.id)
        query = query.filter(ROContainer.name.like("%s%%" % name))
        return [uid for uid, in query.all()]
    elif 'contains' in params or 'use' in params:
        res = ro_search(session, params)
        ros = [ROContainer.get(session, uid) for uid in res]
        return [ro.id for ro in ros if ro is not None]
    else:
        return []
