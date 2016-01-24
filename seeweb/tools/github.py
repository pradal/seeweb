""" All github related functions.
"""

from github3 import login
from github3.models import GitHubError


def ensure_login(user, pwd, owner, project, recursion_ind=0):
    """ Check that the user is logged to github.

    Look for an already registered user. If none found
    ask for credentials and open a new session.
    """
    if recursion_ind > 3:
        raise UserWarning("Pb, infinite recursion in github login")

    gh = login(user, pwd)
    try:
        repo = gh.repository(owner, project)
    except GitHubError:
        print ("bad credentials")
        return ensure_login(user, pwd, owner, project, recursion_ind + 1)

    return gh, repo


def fetch_contributors(repo):
    """ Try to list all contributors for a github project
    """
    info = []
    for user in repo.iter_contributors():
        name = user.name
        if len(name) == 0:
            name = user.login

        info.append((name, user.email))

    return info


def fetch_readme(repo):
    """Find readme information.
    """
    readme = repo.readme()
    if readme is None:
        raise IOError("no readme found")

    return readme.decoded


def fetch_avatar(repo):
    """try to fetch avatar file.
    """
    pth = "avatar.png"
    avatar = repo.contents(pth)
    if avatar is None:
        pth = "avatar_%s.png" % repo.name
        avatar = repo.contents(pth)
        if avatar is None:
            raise IOError("no PNG avatar found")

    return avatar.decoded
