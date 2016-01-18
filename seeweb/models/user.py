# import hashlib
from sqlalchemy import Column, ForeignKey, String, Table, Text
from sqlalchemy.orm import relationship
from models import Base

user_to_projects = Table('asso_user_projects',
                         Base.metadata,
                         Column('user_id', String(255),
                                ForeignKey('user.id'),
                                primary_key=True),
                         Column('project_id', String(255),
                                ForeignKey('project.id'),
                                primary_key=True),
                         )


class User(Base):
    __tablename__ = 'user'

    id = Column("id", String(255), ForeignKey('userid.id'), primary_key=True)

    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)

    description = Column(Text, default="")

    projects = relationship("Project", secondary=user_to_projects)

    def __repr__(self):
        return "<User(id='%s', name='%s', email='%s')>" % (self.id,
                                                           self.name,
                                                           self.email)

    # def md5(self):
    #     return hashlib.md5(self.email.strip().lower()).hexdigest()
