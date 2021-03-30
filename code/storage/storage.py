from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR
from time import sleep
import threading

# Network sockets
sockUDP = socket(AF_INET, SOCK_DGRAM)
sockTCP = socket()

# Network constants
IP_Address = "localhost"
UDP_Port = 5555
TCP_Port = 5556
size = 1024

# Station data
stationData = []


def main():
    startServer()


def startServer():
    # Reuse address
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(("localhost", 5555))

def start_tcp_server():
    # Setup TCP connection
    sockTCP.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockTCP.bind((IP_Address, TCP_Port))
    sockTCP.listen()
    conn, address = sockTCP.accept()
    sleep(15)  # Initial sleep so that we have time to get data from weather station
    while True:
        sleep(1)        # Data polled from the connected client
        sentence = conn.recv(size).decode()
        print(sentence)
        # If something has been sent, sentence will not be empty
        if sentence == "give shit":
            send_weather_in_small_chunks(conn)


def send_weather_in_small_chunks(conn):
    # Get first indices of last items in temperature and precipitation lists
    temperature = stationData[-1][0]
    precipitation = stationData[-1][1]
    for i in range(len(temperature)):
        print(f"tempStorageToClient:{temperature[i]}, precStorageToClient:{precipitation[i]}")
        conn.send(str((temperature[i])).encode())
        conn.send(str((precipitation[i])).encode())


# Poll station updates from weather station through UDP connection
def poll_station_updates():
    while(True):
        temperature = []
        precipitation = []
        for i in range(72):
            rawTemperature, address = sockUDP.recvfrom(size)
            rawPrecipitation, address = sockUDP.recvfrom(size)
            rawTemperature = rawTemperature.decode()
            rawPrecipitation = rawPrecipitation.decode()
            temperature.append(rawTemperature)
            precipitation.append(rawPrecipitation)
            #print(f"temp: {rawTemperature}, prec: {rawPrecipitation}")
        stationData.append((temperature,precipitation))


if __name__ == '__main__':
    main()



