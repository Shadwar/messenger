import logging
import logging.handlers


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
