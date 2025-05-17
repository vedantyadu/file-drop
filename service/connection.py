import socket
import ipaddress
import time
from constants import BROADCAST_PORT, BROADCAST_INTERVAL, SUBNETMASK, PRESENCE_MESSAGE


def get_broadcast_address(self_address: str, subnetmask: str):
    ip = ipaddress.IPv4Interface(f"{self_address}/{subnetmask}")
    return str(ip.network.broadcast_address)


def get_self_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"


def broadcast_presence(self_address: str):
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broadcast_address = get_broadcast_address(self_address, SUBNETMASK)

    while True:
        soc.sendto(PRESENCE_MESSAGE.encode(),
                   (broadcast_address, BROADCAST_PORT))
        time.sleep(BROADCAST_INTERVAL)


def listen_for_peers(self_address: str, available_peers: set):
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.bind((self_address, BROADCAST_PORT))

    while True:
        data, addr = soc.recvfrom(1024)

        if data.decode() == PRESENCE_MESSAGE:
            ip = addr[0]

            if ip != self_address:
                available_peers.add(ip)
