import datetime
import sys

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from server.alchemy import SQLUser, SQLContact


def main(username):
    db_engine = create_engine('sqlite:///server.db')

    total = 0
    data_count = []
    data_date = []

    session = sessionmaker(bind=db_engine)()
    user = session.query(SQLUser).filter(SQLUser.login.ilike(username)).first()
    if user:
        contacts = session.query(SQLContact).filter(SQLContact.user.is_(user.gid)).order_by(SQLContact.created_date.asc()).all()
        for contact in contacts:
            total += 1
            data_count.append(total)
            data_date.append(contact.created_date)

    if data_count:
        fg = plt.figure()
        fg.suptitle('Количество контактов для пользователя {}'.format(username))
        gca = fg.gca()
        gca.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.plot(data_count, data_date)
        plt.show()
    else:
        print('Пользователь не найден, или у него нет контактов')


if __name__ == '__main__':
    args = sys.argv
    if len(args) != 2:
        print('Usage: python3 user_states.py USERNAME')

    username = args[1]

    main(username)