from sqlalchemy import (Boolean, Column, ForeignKey, Index, Integer,
                        PrimaryKeyConstraint, String, Table)
from sqlalchemy.orm import relationship
from models import Base


class Project(Base):
    __tablename__ = 'projects'

    name = Column(String(255), unique=True, primary_key=True)
    owner = Column(String(255), ForeignKey("users.username"), nullable=False)

    public = Column(Boolean)

    def __repr__(self):
        return "<Project(name='%s', owner='%s', public='%s')>" % (self.name,
                                                                  self.owner,
                                                                  self.public)
