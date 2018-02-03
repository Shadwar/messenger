import logging
import logging.handlers


server_log = logging.getLogger('server')
server_log.setLevel(logging.INFO)
server_log.propagate = False
server_log.addHandler(logging.handlers.TimedRotatingFileHandler('server.log', when='D'))
