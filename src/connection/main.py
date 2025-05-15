import socket
import time
import threading
import ipaddress



BROADCAST_INTERVAL = 2
LISTEN_INTERVAL = BROADCAST_INTERVAL * 2

BROADCAST_PORT = 50000
SUBNETMASK = "255.255.255.0"
PRESENCE_MESSAGE = "CONNECTION::HELLO"

available_peers = set()


def get_broadcast_address(self_address: str, subnetmask: str):
    ip = ipaddress.IPv4Interface(f"{self_address}/{subnetmask}")
    return str(ip.network.broadcast_address)


def get_self_address():
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        soc.connect(('8.8.8.8', 80))
        local_network_ip = soc.getsockname()[0]
        return local_network_ip
    finally:
        soc.close()


def broadcast_presence(self_address: str):
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broadcast_address = get_broadcast_address(self_address, SUBNETMASK)

    while True:
        soc.sendto(PRESENCE_MESSAGE.encode(),
                   (broadcast_address, BROADCAST_PORT))
        time.sleep(BROADCAST_INTERVAL)


def listen_for_peers(self_address: str):
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.bind((self_address, BROADCAST_PORT))

    while True:
        data, addr = soc.recvfrom(1024)

        if data.decode() == PRESENCE_MESSAGE:
            ip = addr[0]

            if ip != self_address:
                available_peers.add(ip)


if __name__ == "__main__":
    self_address = get_self_address()
    print(f"Self Address: {self_address}")

    broadcast_thread = threading.Thread(target=broadcast_presence, args=[self_address])
    broadcast_thread.start()

    listen_thread = threading.Thread(target=listen_for_peers, args=[self_address])
    listen_thread.start()

    while True:
        available_peers.clear()
        time.sleep(LISTEN_INTERVAL)
        print("Available peers:", list(available_peers))
        