from socket import socket
from time import sleep
import ast


def main():
    sock = socket()
    server_address = ("localhost", 5556)
    sock.connect(server_address)

    while (True):
        sentence = input("type: give last or give all:\n")
        sock.send(sentence.encode())

        if sentence == "give last":
            rawData = sock.recv(10000).decode()
            temperatureData = ast.literal_eval(rawData[:rawData.index(']') + 1])
            precipitationData = ast.literal_eval(rawData[rawData.index(']') + 1:])
            print(f"tempClient:{temperatureData}\nprecClient:{precipitationData}")

        elif sentence == "give all":
            rawData = sock.recv(1000000).decode()
            num = 1
            while rawData.find(']') > -1:
                temperatureData = ast.literal_eval(rawData[:rawData.index(']') + 1])
                rawData = rawData[rawData.index(']') + 1:]
                precipitationData = ast.literal_eval(rawData[:rawData.index(']') + 1])
                rawData = rawData[rawData.index(']') + 1:]
                print(f"tempClient{num}:{temperatureData}\nprecClient{num}:{precipitationData}")
                num += 1


if __name__ == '__main__':
    main()
