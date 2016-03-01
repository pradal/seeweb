from pyramid.view import view_config


@view_config(route_name='project_content_script_execute',
             renderer='json')
def view(request):
    res = {'a': 10}

    return res
