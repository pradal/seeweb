from project import Project


def create_project(owner, name, public=False):
    """Create a new project.

    args:
     - owner (User): future owner of the project
     - name (str): id of the project
     - public (bool): visibility of the project (default False)

    return:
     - (Project): project has been added to user project list
    """
    project = Project(id=name,
                      owner=owner.id,
                      public=public)

    owner.projects.append(project)

    return project
