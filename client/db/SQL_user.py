from sqlalchemy import Column, Integer, Unicode, BLOB

from client.db.SQL_base import SQLBase


class SQLUser(SQLBase):
    __tablename__ = 'users'

    gid = Column(Integer(), primary_key=True)
    login = Column(Unicode())
    password = Column(Unicode())
    private_key = Column(Unicode())
    public_key = Column(Unicode())
    avatar = Column(BLOB)

    def __repr__(self):
        return 'SQLUser<gid = %d, login = %s, public_key = %s>' % (self.gid, self.login, self.public_key)
