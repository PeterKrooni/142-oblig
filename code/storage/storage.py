import select
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR
from time import sleep
import threading
import ast

# Network sockets
sockUDP = socket(AF_INET, SOCK_DGRAM)
sockTCP = socket()

# Network constants
IP_Address = "localhost"
UDP_Port = 5555
TCP_Port = 5556
size = 10000

# Station data
stationData = []


def main():
    start_udp_server()
    # Run station updates in the background inside another thread
    x = threading.Thread(target=poll_station_updates)
    x.start()
    start_tcp_server()


def start_udp_server():
    # Reuse address
    sockUDP.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockUDP.bind((IP_Address, UDP_Port))


def start_tcp_server():
    # Setup TCP connection
    sockTCP.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockTCP.bind((IP_Address, TCP_Port))
    sockTCP.listen()
    conn, address = sockTCP.accept()
    while not stationData:
        sleep(1)  # Initial sleep so that we have time to get data from weather station
    while True:
        sleep(1)  # Data polled from the connected client
        if not handle_client_tcp_death(conn):
            sentence = conn.recv(size).decode()
            # If something has been sent, sentence will not be empty
            if sentence == "give last":
                send_weather_in_small_chunks(conn)
            elif sentence == "give all":
                send_all_storage(conn)
        else:
            break


# Check if client connection is died a horrible death, if so restart
def handle_client_tcp_death(conn):
    try:
        # Magic select wizardry http://docs.python.org/2/howto/sockets.html#non-blocking-sockets
        select.select([conn, ], [conn], [], 5)
        return False
    except select.error:
        print("Detected client death.")
        conn.shutdown(2)
        conn.close()
        start_tcp_server()
        return True


def send_weather_in_small_chunks(conn):
    # Get first indices of last items in temperature and precipitation lists
    temperature = stationData[-1][0]
    precipitation = stationData[-1][1]

    temp = str(temperature)
    prec = str(precipitation)
    data = temp + prec
    conn.send(data.encode())


def send_all_storage(conn):
    allData = ""
    for x in range(len(stationData)):
        allData = allData + str(stationData[x][0]) + str(stationData[x][1])
    conn.send(allData.encode())

# Poll station updates from weather station through UDP connection
def poll_station_updates():
    while True:
        rawData, address = sockUDP.recvfrom(size)
        rawData = rawData.decode()
        temperature = ast.literal_eval(rawData[:rawData.index(']') + 1])
        precipitation = ast.literal_eval(rawData[rawData.index(']') + 1:])
        stationData.append((temperature, precipitation))
        print("Storage: Received station update!")


if __name__ == '__main__':
    main()
