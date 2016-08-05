from pyramid.httpexceptions import HTTPFound


def view_init(request, session):
    """Common init for all 'view'.

    Args:
        request: (Request)
        session: (DBSession)

    Returns:
        dict of (str: any): view_params
    """
    del session

    if 'main_search' in request.params:
        loc = request.route_url('ro_list', _query=dict(request.params))
        raise HTTPFound(location=loc)

    return {}
