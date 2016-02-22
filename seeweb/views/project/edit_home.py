from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.avatar import load_image, upload_project_avatar
from seeweb.models import DBSession
from seeweb.models.gallery_item import GalleryItem

from .commons import edit_init


@view_config(route_name='project_edit_home',
             renderer='templates/project/edit_home.jinja2')
def view(request):
    session = DBSession()
    project, view_params = edit_init(request, session, 'home')

    if 'update' in request.params:
        if 'description' in request.params:
            project.store_description(request.params['description'])
    elif 'submit_avatar' in request.params:
        field_storage = request.params['avatar']
        if field_storage == "":
            request.session.flash("Select an image first", 'warning')
        else:
            try:
                img = load_image(field_storage)
                upload_project_avatar(img, project)
                request.session.flash("Avatar submitted", 'success')
                loc = request.route_url('project_view_home', pid=project.id)
                return HTTPFound(location=loc)
            except IOError:
                request.session.flash("Unable to read image", 'warning')
    else:
        pass

    # gallery
    items = project.fetch_gallery_items(session)
    for item in list(items):
        if "remove_gallery_item_%s" % item.id in request.params:
            GalleryItem.remove(session, item)
            items.remove(item)

    view_params["gallery"] = items

    return view_params
