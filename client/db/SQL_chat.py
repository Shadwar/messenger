from sqlalchemy import Column, Integer, Unicode

from client.db.SQL_base import SQLBase


class SQLChat(SQLBase):
    __tablename__ = 'chats'

    gid = Column(Integer(), primary_key=True)
    login = Column(Unicode())
    name = Column(Unicode())

    def __repr__(self):
        return 'SQLChat<gid = %d, login = %s, name = %s>' % (self.gid, self.login, self.name)
