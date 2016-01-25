from bs4 import BeautifulSoup
from pyramid.httpexceptions import HTTPFound
import urllib2
from urllib2 import HTTPError
from urlparse import urlsplit, urlunsplit

from seeweb.models.access import get_project, get_user, project_access_role
from seeweb.models.auth import Role

tabs = [('Home', 'home'),
        ('Documentation', 'doc'),
        ('Source', 'source'),
        ('Contributors', 'contributors'),
        ('Comments', 'comments')]


def view_init(request, session, tab):
    """Common init for all 'view' parts
    """
    pid = request.matchdict['pid']

    project = get_project(session, pid)
    if project is None:
        request.session.flash("Project %s does not exists" % pid, 'warning')
        raise HTTPFound(location=request.route_url('home'))

    current_uid = request.unauthenticated_userid
    role = project_access_role(session, project, current_uid)
    if role == Role.denied:
        request.session.flash("Access to %s not granted for you" % pid,
                              'warning')
        raise HTTPFound(location=request.route_url('home'))

    # potential install
    if current_uid is None:  # TODO can do better
        install_action = None
    else:
        user = get_user(session, current_uid)
        if project in user.installed:
            install_action = "uninstall"
        else:
            install_action = "install"

    view_params = {"current_uid": current_uid,
                   "project": project,
                   "tabs": tabs,
                   "tab": tab,
                   "allow_edit": (role == Role.edit),
                   "install_action": install_action,
                   "sections": [],
                   "ratings": project.format_ratings()}

    return project, view_params


def edit_init(request, session, tab):
    """Common init for all 'edit' views.
    """
    project, view_params = view_init(request, session, tab)

    if not view_params["allow_edit"]:
        msg = "Access to %s edition not granted for you" % project.id
        request.session.flash(msg, 'warning')
        raise HTTPFound(location=request.route_url('home'))

    if 'back' in request.params:
        request.session.flash("Edition stopped", 'success')
        loc = request.route_url('project_view_%s' % tab, pid=project.id)
        raise HTTPFound(location=loc)

    if 'delete' in request.params:
        request.session.flash("Edition stopped", 'success')
        loc = request.route_url('home')
        raise HTTPFound(location=loc)

    return project, view_params


def edit_common(request, session, project):
    """Common edition operations
    """
    del session

    # edit team visibility
    public = 'visibility' in request.params
    project.public = public

    return False


def fetch_documentation(url, pid):
    """Try to fetch documentation from given url
    return html home page for doc
    """
    try:
        scheme = urlsplit(url).scheme
        netloc = "%s.readthedocs.org/en/latest" % pid

        response = urllib2.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")
        section = soup.find('div', {'class': 'section'})
        if section is None:
            return None

        for link in section.find_all('a'):
            url = urlsplit(link["href"])
            if url.netloc == "":
                link["href"] = urlunsplit((scheme, netloc) + url[2:])

        txt = section.prettify()
        return txt
    except HTTPError:
        return None
