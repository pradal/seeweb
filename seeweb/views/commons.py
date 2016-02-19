from pyramid.httpexceptions import HTTPFound

from seeweb.models.team import Team
from seeweb.models.user import User


def view_init(request, session):
    """Common init for all 'view'.

    Args:
        request: (Request)
        session: (DBSession)

    Returns:
        dict of (str: any): view_params
    """
    search_pattern = request.params.get("main_search", "")
    if search_pattern != "":
        user = User.get(session, search_pattern)
        if user is not None:
            loc = request.route_url('user_view_home', uid=user.id)
            return HTTPFound(location=loc)

        team = Team.get(session, search_pattern)
        if team is not None:
            loc = request.route_url('team_view_home', tid=team.id)
            return HTTPFound(location=loc)

        loc = request.route_url('project_list',
                                _query={"main_search": search_pattern})
        return HTTPFound(location=loc)

    return {}
