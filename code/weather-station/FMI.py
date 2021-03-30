from socket import socket
from time import sleep

def main():
    sock = socket()
    server_address = ("localhost", 5556)
    sock.connect(server_address)

    sentence = input("give shit or give all shit:\n")

    sock.send(sentence.encode())

    while(True):
        temperatureData = sock.recv(1024).decode()
        precipitationData = sock.recv(1024).decode()
        print(f"tempClient:{temperatureData}, precClient:{precipitationData}")

if __name__ == '__main__':
    main()