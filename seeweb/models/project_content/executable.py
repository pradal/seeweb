from sqlalchemy import Column, ForeignKey, Integer, String

from ...models import Base


class Executable(Base):
    """Store the properties of a console script.
    """
    __tablename__ = 'executables'

    id = Column(Integer, autoincrement=True, primary_key=True)
    cnt = Column(Integer, ForeignKey("pjt_contents.id"), nullable=False)
    name = Column(String(255), nullable=False)

    def __repr__(self):
        return "<Executable(id='%s')>" % self.id
