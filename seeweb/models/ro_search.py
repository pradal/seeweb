from seeweb.models.research_object import ResearchObject
from seeweb.models.ro_link import ROLink


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
        query = session.query(ResearchObject.id)
        query = query.filter(ResearchObject.name.like("%s%%" % name))
        return [uid for uid, in query.all()]
    elif 'contains' in params:
        # search all RO that contains a specific id
        uid = params['contains']
        query = session.query(ROLink.source)
        query = query.filter(ROLink.target == uid,
                             ROLink.type == 'contains')
        return [uid for uid, in query.all()]
    elif 'use' in params:
        # search all RO that use a specific id
        uid = params['use']
        query = session.query(ROLink.source)
        query = query.filter(ROLink.target == uid,
                             ROLink.type == 'use')
        return [uid for uid, in query.all()]
    else:
        return []
