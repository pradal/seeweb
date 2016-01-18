from sqlalchemy import Column, ForeignKey, Integer, String
from models import Base


class Actor(Base):
    __tablename__ = 'actor'

    id = Column(Integer, autoincrement=True, primary_key=True)
    user = Column(String(255), ForeignKey("userid.id"), nullable=False)
    role = Column(Integer)

    def __repr__(self):
        return "<User(id='%s', user='%s', role='%s')>" % (self.id,
                                                          self.user,
                                                          self.role)
