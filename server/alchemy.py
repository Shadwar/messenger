from sqlalchemy import Column, Integer, Unicode, UniqueConstraint, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship, defer, load_only
from sqlalchemy.ext.declarative import declarative_base


SQLBase = declarative_base()


class SQLUser(SQLBase):
    __tablename__ = 'users'

    gid = Column(Integer(), primary_key=True)
    login = Column(Unicode())
    password = Column(Unicode())

    check_1 = UniqueConstraint('login')

    def __repr__(self):
        return 'SQLUser<gid = %d, login = %s, password=%s>' % (self.gid, self.login, self.password)


class SQLMessage(SQLBase):
    __tablename__ = 'messages'

    gid = Column(Integer(), primary_key=True)
    u_from = Column(Integer(), ForeignKey('users.gid'))
    u_to = Column(Integer(), ForeignKey('users.gid'))
    time = Column(Integer())
    message = Column(Unicode())

    p_u_from = relationship("SQLUser", foreign_keys=[u_from])
    p_u_to = relationship("SQLUser", foreign_keys=[u_to])

    def __repr__(self):
        return 'SQLMessage<gid = %d, u_to = %d, u_from = %d, message = %s>' % (self.gid, self.u_to, self.u_from, self.message)


class SQLChat(SQLBase):
    __tablename__ = 'chats'

    gid = Column(Integer(), primary_key=True)
    name = Column(Unicode())

    def __repr__(self):
        return 'SQLChat<gid = %d, name = %s' % (self.gid, self.name)


class SQLChatMessage(SQLBase):
    __tablename__ = 'chat_messages'

    gid = Column(Integer(), primary_key=True)
    u_from = Column(Integer(), ForeignKey('users.gid'))
    u_to = Column(Integer(), ForeignKey('chats.gid'))
    message = Column(Unicode())

    p_u_from = relationship("SQLUser", foreign_keys=[u_from])
    p_u_to = relationship("SQLChat", foreign_keys=[u_to])

    def __repr__(self):
        return 'SQLChatMessage<gid = %d, u_to = %d, u_from = %d, message = %s>' % (self.gid, self.u_to, self.u_from, self.message)


class SQLUserChat(SQLBase):
    __tablename__ = 'users_chats'

    gid = Column(Integer(), primary_key=True)
    user = Column(Integer(), ForeignKey('users.gid'))
    chat = Column(Integer(), ForeignKey('chats.gid'))

    p_user = relationship("SQLUser", foreign_keys=[user])
    p_chat = relationship("SQLChat", foreign_keys=[chat])

    def __repr__(self):
        return 'SQLUserChat<user = %d, chat = %d>' % (self.user, self.chat)


class SQLContact(SQLBase):
    __tablename__ = 'contacts'

    gid = Column(Integer(), primary_key=True)
    user = Column(Integer(), ForeignKey('users.gid'))
    contact = Column(Integer(), ForeignKey('users.gid'))

    p_user = relationship("SQLUser", foreign_keys=[user])
    p_contact = relationship("SQLUser", foreign_keys=[contact])

    def __repr__(self):
        return 'SQLContact<user = %d, contact = %d>' % (self.user, self.contact)
