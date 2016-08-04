from glob import glob
from importlib import import_module
from os.path import basename, exists, splitext


from seeweb.models import ro_search
from seeweb.models.research_object import ResearchObject
from seeweb.models.ro_link import ROLink


# construct RO factory
search_factory = dict(ro=ro_search.search)

for topdir in ("ro", "rodata"):
    for dname in glob("seeweb/%s/*/" % topdir):
        dname = dname.replace("\\", "/")

        if exists(dname + "search.py"):
            modname = dname.replace("/", ".") + "search"
            search_mod = import_module(modname)
            for model_pth in glob(dname + "models/*.py"):
                filename = splitext(basename(model_pth))[0]
                if filename != "__init__":
                    modname = splitext(model_pth)[0].replace("/", ".")
                    mod = import_module(modname)
                    if hasattr(mod, "__all__"):
                        for name in mod.__all__:
                            RO = getattr(mod, name)
                            typ = RO.__mapper_args__['polymorphic_identity']
                            search_factory[typ] = search_mod.search


def search(session, params):
    """Perform a query for RO objects

    Args:
        session (DBSession):
        params (dict): extra parameters for search

    Returns:
        (list of str): list of ids of RO matching query
    """
    # query on RO direct common attributes
    query = session.query(ResearchObject.id)
    if "type" in params:
        query = query.filter(ResearchObject.type == params["type"])

    if "owner" in params:
        query = query.filter(ResearchObject.owner == params["owner"])

    if "name" in params:
        name = params['name']
        if name[-1] == "*":
            name = name[:-1]
            query = query.filter(ResearchObject.name.like("%s%%" % name))
        else:
            query = query.filter(ResearchObject.name == name)

    # query = query.order_by(ResearchObject.name)

    uids = {uid for uid, in query.all()}

    # query on type of link
    if 'in' in params:
        # search all RO in a specific container
        uid = params['in']
        query = session.query(ROLink.target)
        query = query.filter(ROLink.source == uid, ROLink.type == 'contains')
        uids &= {uid for uid, in query.all()}

    if 'use' in params:
        # search all RO that use a specific id
        uid = params['use']
        query = session.query(ROLink.source)
        query = query.filter(ROLink.target == uid, ROLink.type == 'use')
        uids &= {uid for uid, in query.all()}

    # specific query by type
    if "type" in params:
        typ = params['type']
        if typ in search_factory:
            print "typed", typ, search_factory[typ], "\n" * 10

    # fetch ROs
    res = [ResearchObject.get(session, uid) for uid in uids]

    # high level python expressed query
    if "toplevel" in params:
        res = [ro for ro in res if ro.is_lonely()]

    # sort by name
    res = sorted([(ro.name, ro) for ro in res])

    return [ro for name, ro in res]
