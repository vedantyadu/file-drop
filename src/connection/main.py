import socket
import time
import threading

BROADCAST_INTERVAL = 2
LISTEN_INTERVAL = BROADCAST_INTERVAL * 2

BROADCAST_PORT = 50000
PRESENCE_MESSAGE = "CONNECTION::HELLO"

available_peers = set()


def get_self_ip():
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        soc.connect(('8.8.8.8', 80))
        local_network_ip = soc.getsockname()[0]
        
        return local_network_ip
    finally:
        soc.close()


def broadcast_presence():
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    while True:
        soc.sendto(PRESENCE_MESSAGE.encode(), ('255.255.255.255', BROADCAST_PORT))
        time.sleep(BROADCAST_INTERVAL)


def listen_for_peers(self_ip: str):
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.bind((self_ip, BROADCAST_PORT))
    print(soc)

    while True:
        data, addr = soc.recvfrom(1024)

        if data.decode() == PRESENCE_MESSAGE:
            ip = addr[0]

            if ip != self_ip:
                available_peers.add(ip)


if __name__ == "__main__":
    self_ip = get_self_ip()
    print(f"Self IP: {self_ip}")

    broadcast_thread = threading.Thread(target=broadcast_presence)
    broadcast_thread.start()

    listen_thread = threading.Thread(target=listen_for_peers, args=[self_ip])
    listen_thread.start()

    while True:
        available_peers.clear()
        time.sleep(LISTEN_INTERVAL)
        print("Available peers:", list(available_peers))
