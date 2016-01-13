
def get_current_uid(request):
    """Fetch user_id of currently logged user.

    Return None if no user logged in.
    """
    return request.session.get("userid", None)


def set_current_uid(request, uid):
    """Set the currently logged user
    """
    request.session["userid"] = uid
