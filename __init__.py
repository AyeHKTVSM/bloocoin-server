__version__ = "1.2.1-stable"

import socket
import get_coin
import send_coin
import my_coins
import check
import transactions
import time
import threading
import register
import json
import total_coins
import check_addr

# Note: When adding new commands, increment the Y of the
# __version__ above.
ncmds = {
    "get_coin": get_coin.GetCoin,
    "register": register.Register,
    "send_coin": send_coin.SendCoin,
    "my_coins": my_coins.MyCoins,
    "check": check.Check,
    "transactions": transactions.Transactions,
    "total_coins": total_coins.TotalCoins,
    "check_addr": check_addr.CheckAddr,
}


def main():
    port = 3122
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', port))

    sock.listen(5)
    while True:
        obj, conn = sock.accept()
        threading.Thread(target=handle, args=(obj, conn)).start()


def handle(obj, conn):  # Function for parsing commands, {'cmd':command}
    try:
        data = obj.recv(1024)
    except Exception as e:
        obj.close()
        return
    if not data:
        return
    print(conn[0], data.decode('utf-8'))
    try:
        d = json.loads(data)
        cmd = ncmds[d['cmd']](obj, data)
        if cmd._handle:
            cmd.handle()
    except ValueError as e:
        # If there's a decoding error, send them a reply,
        # so they're not just left hanging.
        obj.sendall(json.dumps({
            "success": False,
            "message": "Unable to parse JSON request",
            "payload": {
                "request": data.decode('utf-8')
            }
        }).encode('utf-8'))
    except Exception as e:
        # If data is not in the JSON format it will log the error.
        print(e)

if __name__ == "__main__":
    main()
