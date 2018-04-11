from sqlalchemy import Column, Integer, Unicode

from client.db.SQL_base import SQLBase


class SQLMessage(SQLBase):
    __tablename__ = 'messages'

    gid = Column(Integer(), primary_key=True)
    user = Column(Unicode())
    u_from = Column(Unicode())
    u_to = Column(Unicode())
    time = Column(Integer())
    message = Column(Unicode())

    def __repr__(self):
        return 'SQLMessage<gid = %d, u_from = %s, u_to = %s, message = %s>' % (self.gid, self.u_from, self.u_to, self.message)
