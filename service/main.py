import time
import threading
from connection import get_self_address, broadcast_presence, listen_for_peers
from constants import LISTEN_INTERVAL
import json


def main():
    self_address = get_self_address()
    available_peers = set()

    broadcast_thread = threading.Thread(
        target=lambda:broadcast_presence(self_address),
    )
    broadcast_thread.start()

    listen_thread = threading.Thread(
        target=lambda:listen_for_peers(self_address, available_peers),
    )
    listen_thread.start()

    while True:
        available_peers.clear()
        time.sleep(LISTEN_INTERVAL)
        print(json.dumps(lambda address: {"address": address, id: ""}), map(list(available_peers)), flush=True, end="")


if __name__ == "__main__":
    main()
