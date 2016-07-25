from seeweb.models.ro_link import ROLink
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
    elif 'consume' in params:
        # search all RO that have consumed the given data
        uid = params['consume']
        query = session.query(ROLink.source)
        query = query.filter(ROLink.target == uid,
                             ROLink.type == 'consume')
        return [uid for uid, in query.all()]
    elif 'produce' in params:
        # search all RO that have been produced by an execution
        uid = params['produce']
        query = session.query(ROLink.target)
        query = query.filter(ROLink.source == uid,
                             ROLink.type == 'produce')
        return [uid for uid, in query.all()]
    elif 'use' in params:
        # search all RO that use a specific id
        uid = params['use']
        query = session.query(ROLink.source)
        query = query.filter(ROLink.target == uid,
                             ROLink.type == 'use')
        # TODO filter on workflow_prov
        return [uid for uid, in query.all()
                if ROWorkflowProv.get(session, uid) is not None]
    else:
        return []
