from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR

sock = socket(AF_INET, SOCK_DGRAM)
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sock.bind(("localhost", 5555))

while True:
    name, address = sock.recvfrom(1000)
    name = name.decode()
    name = name+" penis"

    sock.sendto(name.encode(), address)