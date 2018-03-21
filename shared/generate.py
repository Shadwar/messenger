import hashlib


def get_hash(login, password):
    """
    Возвращает хеш логина и пароля
    :param login:
    :param password:
    :return:
    """
    msg = hashlib.sha256()
    msg.update(login.encode())
    msg.update(password.encode())

    h = msg.hexdigest()
    return h
