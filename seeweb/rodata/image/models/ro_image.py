from sqlalchemy import Column, ForeignKey, String

from seeweb.models.models import get_by_id
from seeweb.ro.data.models.ro_data import ROData


__all__ = ["ROImage"]


class ROImage(ROData):
    """Research Object of type png image
    """
    __tablename__ = 'ro_images'

    id = Column(String(255), ForeignKey('ro_datas.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'image',
    }

    def __repr__(self):
        return "<ROImage(id='%s'')>" % self.id

    @staticmethod
    def get(session, uid):
        """Fetch a given RO in the database.

        Args:
            session: (DBSession)
            uid: (str) RO id

        Returns:
            (ResearchObject) or None if no RO with this id is found
        """
        return get_by_id(session, ROImage, uid)
