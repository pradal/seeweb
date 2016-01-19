from bs4 import BeautifulSoup
from pyramid.httpexceptions import HTTPFound
import urllib2
from urllib2 import HTTPError
from urlparse import urlsplit, urlunsplit

from seeweb.models.access import get_project, project_access_role
from seeweb.models.auth import Role
from seeweb.views.tools import get_current_uid

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

    current_uid = get_current_uid(request)
    role = project_access_role(session, project, current_uid)
    if role == Role.denied:
        request.session.flash("Access to %s not granted for you" % pid,
                              'warning')
        raise HTTPFound(location=request.route_url('home'))

    view_params = {"project": project,
                   "tabs": tabs,
                   "tab": tab,
                   "allow_edit": (role == Role.edit),
                   "sections": [],
                   "ratings": project.format_ratings()}

    if current_uid is not None:
        view_params["current_uid"] = current_uid

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
