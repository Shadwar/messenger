from sqlalchemy import Column, Integer, Unicode, UniqueConstraint, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


SQLBase = declarative_base()


class SQLContact(SQLBase):
    __tablename__ = 'contacts'

    gid = Column(Integer(), primary_key=True)
    login = Column(Unicode())
    contact = Column(Unicode())

    def __repr__(self):
        return 'SQLContact<gid = %d, login = %s, contact = %s' % (self.gid, self.login, self.contact)


class SQLMessage(SQLBase):
    __tablename__ = 'messages'

    gid = Column(Integer(), primary_key=True)
    user = Column(Unicode())
    u_from = Column(Unicode())
    u_to = Column(Unicode())
    message = Column(Unicode())

    def __repr__(self):
        return 'SQLMessage<gid = %d, u_from = %s, u_to = %s, message = %s' % (self.gid, self.u_from, self.u_to, self.message)
