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
