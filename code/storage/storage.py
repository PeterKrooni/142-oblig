from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR
from time import sleep

sock = socket(AF_INET, SOCK_DGRAM)

# Station data
stationData = [([], [])]

def main():
    startServer()


def startServer():
    # Reuse address
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(("localhost", 5555))

    # Start station polling
    while True:
        pollStationUpdates()

        # Delay until next poll
        sleep(5)


def pollStationUpdates():
    for size in range (1, 72):
        rawData = sock.recvfrom()
        stationData.append(rawData.decode())
        print(f"Recived from weather station.")

