import sys
from server.server import Server
import shared.log_config

if __name__ == '__main__':
    args = sys.argv
    # Получаем ip и port из коммандной строки,
    # показывать ошибку, если ip не указан
    if len(args) not in (3, 5):
        print("Ошибка запуска сервера:")
        print("server.py -a addr [-p port]")
        sys.exit()

    addr = '127.0.0.1'
    port = 7777
    for i, s in enumerate(args):
        if s == '-a':
            addr = args[i+1]
        elif s == '-p':
            port = int(args[i+1])

    shared.log_config.init()
    server = Server(addr, port)
    server.run()
