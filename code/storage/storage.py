import select
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR
from time import sleep
import threading
import ast
import os

# Network sockets
sockUDP = socket(AF_INET, SOCK_DGRAM)
sockTCP = socket()

# Network constants
IP_Address = "localhost"
UDP_Port = 5555
TCP_Port = 5556
size = 10000

# Station data
storage_file = "storage.txt"


def main():
    make_storage_file()
    start_udp_server()
    # Run station updates in the background inside another thread
    x = threading.Thread(target=poll_station_updates)
    x.start()
    start_tcp_server()


def make_storage_file():
    """
    Creates a new file called storage.txt for storing all data received from the weather station.
    If the files already exists it overwrites the content so that the file is empty.

    :rtype: None
    """

    with open(storage_file, "w") as file:
        file.write("")


def start_udp_server():
    """
    Initializes the UDP server and binds it to the port and ip address
    UDP server connects with the weather station to receive data

    :rtype: None
    """

    sockUDP.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockUDP.bind((IP_Address, UDP_Port))


def start_tcp_server():
    """
    Initializes TCP Server for connection with client
    Sends storage in formats depending on sentence received from client

    :rtype: None
    """

    # Setup TCP connection
    sockTCP.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockTCP.bind((IP_Address, TCP_Port))
    sockTCP.listen()
    conn, address = sockTCP.accept()

    with open(storage_file, "w+") as file:
        while file.read() == "":
            sleep(1)  # Initial sleep so that we have time to get data from weather station

    while True:
        sleep(1)  # Data polled from the connected client
        if not handle_client_tcp_death(conn):

            # Receive a signal from the FMI client about what information to send
            sentence = conn.recv(size).decode()
            if sentence == "give last":
                send_last_weather_data(conn)
            elif sentence == "give all":
                send_all_storage(conn)
        else:
            break


def handle_client_tcp_death(conn):
    """
    Checks if TCP connection is still connected

    :return: true if client connection is dead, false if connection is still going
    :rtype: bool
    :param connection conn: TCP connection to check

    :rtype: Boolean
    """

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


def send_last_weather_data(conn):
    """
    Sends latest entry in storage file

    :param connection conn: TCP Connection to client
    :rtype: None
    """

    with open(storage_file, "r") as file:
        line_list = file.readlines()
        # Gets the last two entries in the storage and sends them to the client
        temp = line_list[-2]
        prec = line_list[-1]
        data = temp + prec
        conn.send(data.encode())


def send_all_storage(conn):
    """
    Sends all entries in storage file

    :param connection conn: TCP Connection to client
    :rtype: None
    """

    allData = ""
    with open(storage_file, "r") as file:
        line_list = file.readlines()
        for line in line_list:
            allData = allData + line
    conn.send(allData.encode())


def poll_station_updates():
    """
    Poll station updates from weather station through UDP connection,
    decodes station data and writes to storage log if received

    :rtype: None
    """

    while True:
        rawData, address = sockUDP.recvfrom(size)
        rawData = rawData.decode()
        temperature = ast.literal_eval(rawData[:rawData.index(']') + 1])
        precipitation = ast.literal_eval(rawData[rawData.index(']') + 1:])
        with open(storage_file, "a") as file:
            file.write(str(temperature)+'\n')
            file.write(str(precipitation)+'\n')
        print("Storage: Received station update!")


if __name__ == '__main__':
    main()
