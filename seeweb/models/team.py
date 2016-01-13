from sqlalchemy import Boolean, Column, String
from models import Base


class Team(Base):
    __tablename__ = 'teams'

    name = Column(String(255), unique=True, primary_key=True)
    public = Column(Boolean)

    def __repr__(self):
        return "<Team(name='%s', public='%s')>" % (self.name, self.public)
