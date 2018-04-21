from sqlalchemy import Column, Integer, Unicode

from .SQL_base import SQLBase


class SQLContact(SQLBase):
    __tablename__ = 'contacts'
    print('kivy_client_db_SQL_contact')

    gid = Column(Integer(), primary_key=True)
    login = Column(Unicode())
    contact = Column(Unicode())
    public_key = Column(Unicode())

    def __repr__(self):
        return 'SQLContact<gid = %d, login = %s, contact = %s>' % (self.gid, self.login, self.contact)
