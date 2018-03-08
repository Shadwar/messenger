import logging
import logging.handlers
from functools import wraps
import logging
import time
import inspect


def log(func):
    """ Логирует вызовы к функциям """
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger('server_decorated')

        all_args = []
        for arg in args:
            all_args.append(str(arg))
        for k, i in kwargs.items():
            all_args.append('{}={}'.format(k, i))

        params = {
            'asctime': time.ctime(),
            'levelname': 'INFO',
            'modulename': func.__module__,
            'funcname': func.__name__,
            'args': ','.join(all_args)
        }
        logger.info('%(asctime)s %(levelname)-10s %(modulename)s %(funcname)s %(args)s', params)
        return func(*args, **kwargs)

    return wrapper


def init():
    server_log = logging.getLogger('server')
    server_log.setLevel(logging.INFO)
    server_log.propagate = False
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    handler.setFormatter(formatter)
    server_log.addHandler(handler)

    server_dec_log = logging.getLogger('server_decorated')
    server_dec_log.setLevel(logging.INFO)
    server_dec_log.propagate = False
    server_dec_log.addHandler(logging.handlers.TimedRotatingFileHandler('server.log', when='D'))
