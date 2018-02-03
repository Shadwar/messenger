from functools import wraps
import logging
import time
import inspect


def log(func):
    """ Логирует вызовы к функциям """
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(dir(func))
        logger = logging.getLogger('server')

        all_args = []
        for arg in args:
            all_args.append(str(arg))
        for k, i in kwargs.items():
            all_args.append('{}={}'.format(k, i))

        params = {
            'asctime': time.ctime(),
            'levelname': logging.INFO,
            'modulename': func.__module__,
            'funcname': func.__name__,
            'args': ','.join(all_args)
        }
        logger.info('%(asctime)s %(levelname)-10s %(modulename)s %(funcname)s %(args)s', params)
        return func(*args, **kwargs)

    return wrapper
