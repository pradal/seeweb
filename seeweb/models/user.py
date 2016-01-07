from sqlalchemy import (Column, ForeignKey, Index, Integer,
                        PrimaryKeyConstraint, String, Table)
from sqlalchemy.orm import relationship
from models import Base
# from project import Project

user_to_pjts = Table('asso_user_pjts',
                     Base.metadata,
                     Column('user_id', Integer, ForeignKey('users.id'),
                            primary_key=True),
                     # Column('pjt_id', Integer, ForeignKey('projects.id'),
                     #        primary_key=True),
                     # PrimaryKeyConstraint('user_id', 'pjt_id')
                     )


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    display_name = Column(String(255))
    # projects = relationship("Project", secondary=user_to_pjts)

    def __repr__(self):
        return "<User(id='%s', name='%s', email='%s')>" % (self.id,
                                                           self.display_name,
                                                           self.email)


Index('user_index', User.display_name, unique=True, mysql_length=255)
