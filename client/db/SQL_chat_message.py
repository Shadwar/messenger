from sqlalchemy import Column, Integer, Unicode

from client.db.SQL_base import SQLBase


class SQLChatMessage(SQLBase):
    __tablename__ = 'chat_messages'

    gid = Column(Integer(), primary_key=True)
    login = Column(Unicode())
    name = Column(Unicode())
    contact = Column(Unicode())
    time = Column(Integer())
    message = Column(Unicode())

    def __repr__(self):
        return 'SQLChatMessage<gid = %d, name = %s, contact = %s, message = %s>' % (self.gid, self.name, self.contact, self.message)
