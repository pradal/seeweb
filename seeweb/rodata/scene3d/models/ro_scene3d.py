from sqlalchemy import Column, ForeignKey, String

from seeweb.models.models import get_by_id
from seeweb.ro.data.models.ro_data import ROData


__all__ = ["ROScene3d"]


class ROScene3d(ROData):
    """Research Object to display 3D stuff
    """
    __tablename__ = 'ro_scene3d'

    id = Column(String(255), ForeignKey('ro_datas.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'scene3d',
    }

    implements = "b6bc57f0595811e6a3a6d4bed973e64a"

    def __repr__(self):
        return "<ROScene3d(id='%s')>" % (self.id,)

    @staticmethod
    def get(session, uid):
        """Fetch a given RO in the database.

        Args:
            session: (DBSession)
            uid: (str) RO id

        Returns:
            (ResearchObject) or None if no RO with this id is found
        """
        return get_by_id(session, ROScene3d, uid)
