from socket import socket, AF_INET, SOCK_DGRAM
from time import sleep

sock = socket(AF_INET, SOCK_DGRAM)
name = "Stor"

server_address = ("localhost", 5555)
while True:
    sleep(1)
    sock.sendto(name.encode(), server_address)
    name, address = sock.recvfrom(1000)
    name = name.decode()
    print("number is" + name)
