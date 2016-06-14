from sqlalchemy import Column, ForeignKey, Integer, String

from .models import Base


class ROLink(Base):
    """Base class for all links between research objects
    """
    __tablename__ = 'ro_links'

    id = Column(Integer, autoincrement=True, primary_key=True)
    source = Column(String(32), ForeignKey("ros.id"))
    target = Column(String(32), ForeignKey("ros.id"))
    type = Column(String(50), default="use")

    def __repr__(self):
        return "<ROLink(id='%s', source='%s', target='%d')>" % (self.id,
                                                                self.source,
                                                                self.target)

    @staticmethod
    def connect(session, sid, tid, typ):
        """Create a new link between two ROs.

        Args:
            session: (DBSession)
            sid: (str) id of source RO
            tid: (str) id of target RO
            typ: (str) link type

        Returns:
            (ROLink)
        """
        link = ROLink(source=sid, target=tid, type=typ)
        session.add(link)

        return link

    @staticmethod
    def remove(session, link):
        """Remove a link between two ROs from database.

        Args:
            session: (DBSession)
            link: (ROLink)

        Returns:
            (True)
        """
        # remove link
        session.delete(link)

        return True
