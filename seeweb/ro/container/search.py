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
    if 'title' in params:
        # search all RO whose title starts with something similar
        title = params['title']
        query = session.query(ROContainer.id)
        query = query.filter(ROContainer.title.like("%s%%" % title))
        return [uid for uid, in query.all()]
    elif 'contains' in params or 'use' in params:
        res = ro_search(session, params)
        for uid in res:
            print "ROC", uid, ROContainer.get(session, uid), "\n" * 10
        ros = [ROContainer.get(session, uid) for uid in res]
        return [ro.id for ro in ros if ro is not None]
    else:
        return []
