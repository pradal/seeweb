"""Functions used to manage security at view level

Used only to grant access to the admin part of the website

For other aspect, the auth is managed locally.
"""
from pyramid.httpexceptions import HTTPFound
from pyramid.security import forget, remember


def is_good_id(txt):  # TODO
    """Check whether txt is good to use as id.

    Args:
        txt: (str) a string

    Returns:
        (bool)
    """
    return " " not in txt


def is_good_name(txt):  # TODO
    """Check whether txt is good to use as name.

    Args:
        txt: (str) a string

    Returns:
        (bool)
    """
    return " " not in txt


def is_good_email(txt):  # TODO
    """Check whether txt is good to use as email.

    Args:
        txt: (str) a string

    Returns:
        (bool)
    """
    return " " not in txt


def groupfinder(userid, request):
    """Find which group the user belongs to.

    Function called automatically by the pyramid framework.

    Args:
        userid: (str)
        request: (Request)

    Returns:
        (list of str)
    """
    if userid == 'revesansparole':  # TODO add a table to allow dynamic changes
        return ['group:admins']


def check_password(session, user, pwd):
    """Check that the given password correspond to the given user

    Args:
        session: (DBSession)
        user: (User)
        pwd: (str)

    Returns:
        (Bool): True if password correspond to user password
    """
    del session
    return pwd[0] == user.id[0]


def log_user_in(request, uid, edit=False):
    """Perform login, assume all credentials are OK.


    Args:
        request: (Request)
        uid: (str) user id
        edit: (bool) default False, whether to redirect to edit page
              or just user home page.

    Returns:
        (HTTPFound)
    """
    headers = remember(request, uid)
    if edit:
        loc = request.route_url('user_edit_home', uid=uid)
    else:
        loc = request.route_url('user_view_home', uid=uid)

    return HTTPFound(location=loc, headers=headers)


def log_user_out(request):
    """Log the current user out.


    Args:
        request: (Request)

    Returns:
        (HTTPFound)
    """
    headers = forget(request)
    return HTTPFound(location=request.route_url('home'),
                     headers=headers)


# useless since cannot be called from templates!
# def current_user(request):
#     """Returns current user id.
#
#     Args:
#         request: (Request)
#
#     Returns:
#         (str) current user id
#         (None) if no user logged in
#     """
#     return request.unauthenticated_userid
