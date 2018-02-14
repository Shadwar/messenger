import sys
from client.client import Client

if __name__ == '__main__':
    args = sys.argv

    if len(args) not in (2, 3):
        print("Ошибка запуска клиента:")
        print("client.py addr [port]")
        sys.exit()

    addr = args[1]

    try:
        port = int(args[2])
    except Exception:
        port = 7777

    client = Client(addr, port)
    client.run()
