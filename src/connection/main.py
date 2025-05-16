import time
import threading
from connection import get_self_address, broadcast_presence, listen_for_peers
from constants import LISTEN_INTERVAL


def main():
    self_address = get_self_address()
    available_peers = set()

    print(f"Self Address: {self_address}")

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
        print("Available peers:", list(available_peers))


if __name__ == "__main__":
    main()
