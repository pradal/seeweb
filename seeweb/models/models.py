from pyramid.security import Allow, Everyone
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class RootFactory(object):
    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, 'group:admins', 'admin')]

    def __init__(self, request):
        pass


def get_by_id(session, object_type, obj_id):
    """Internal function used to retrieve an object from
    the database using its id.

    Args:
        session: (DBSession)
        object_type: (Class)
        obj_id: (any)

    Returns:
        (Object or None) if no object found
    """
    if obj_id is None:
        return None

    items = session.query(object_type).filter(object_type.id == obj_id).all()
    if len(items) == 0:
        return None

    item, = items

    return item
