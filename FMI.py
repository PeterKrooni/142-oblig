import os
import threading
from socket import socket
from time import sleep
import ast


def main():
    """
    Entry point for application
    Writes a prompt to the console which asks user which mode they wish to start the application
    Starts storage and weather station server in CLI mode

    :rtype: None
    """

    print_console_information()
    mode = input("> Type "
                 + '\033[93m' + "'cli' " + '\033[0m'
                 + "or "
                 + '\033[93m' + "'web' " + '\033[0m')

    if mode == "web":
        print("web")
        os.system("python code/app.py")

    elif mode == "cli":
        print("Starting storage and weather services...")
        start_station_and_storage_threads()
        sock = init_socket_connection()

        while True:
            sentence = input("> type: give last or give all:\n")

            # Sends signal to storage about whether we want the last data from storage or alle the data
            sock.send(sentence.encode())

            if sentence == "give last":
                print_last_data_from_storage(sock.recv(100000).decode())
            elif sentence == "give all":
                print_all_data_from_storage(sock.recv(1000000).decode())


def print_last_data_from_storage(rawData):
    """
    Takes a string of two lists containing temperature data and precipitation data and splits it into single lists
    of temperature data and precipitation data. Then prints the lists to console

    :rtype: None
    """

    temperatureData = ast.literal_eval(rawData[:rawData.index(']') + 1])
    precipitationData = ast.literal_eval(rawData[rawData.index(']') + 1:])
    print(f"tempClient:{temperatureData}\nprecClient:{precipitationData}")


def print_all_data_from_storage(rawData):
    """
    Takes a string of multiple lists containing temperature data and precipitation data and splits it into single lists
    of temperature data and precipitation data. Then prints the lists to console

    :rtype: None
    """

    num = 1
    while rawData.find(']') > -1:
        temperatureData = ast.literal_eval(rawData[:rawData.index(']') + 1])
        rawData = rawData[rawData.index(']') + 1:]
        precipitationData = ast.literal_eval(rawData[:rawData.index(']') + 1])
        rawData = rawData[rawData.index(']') + 1:]
        print(f"tempClient{num}:{temperatureData}\nprecClient{num}:{precipitationData}")
        num += 1


def start_station_and_storage_threads():
    """
    Starts the storage and the weather station servers in other threads

    :rtype: None
    """

    ws = threading.Thread(target=run_weather_station)
    s = threading.Thread(target=run_storage)
    ws.start()
    s.start()

    # Gives the storage thread and weather station threads time initialize
    sleep(2)


def print_console_information():
    """
    Prints information about what interface the users wants to use

    :rtype: None
    """

    print('\033[92m' + "> Welcome to the FMI client!" + '\033[0m')
    print("> You can choose either a"
          + '\033[94m' + " command line interface" + '\033[0m'
          + " mode, or a "
          + '\033[94m' + "web app mode" + '\033[0m')
    print("> CLI shows data in this console, while web app mode is a web app that shows data as graphs on a website.")


def init_socket_connection():
    """
    Starts the TCP socket and connects it to the server

    :rtype: socket
    """

    sock = socket()
    server_address = ("localhost", 5556)
    sock.connect(server_address)
    return sock


def run_weather_station():
    """
    Run weather station server

    :rtype: None
    """

    os.system("python code/weather-station/weather-station-server.py")


def run_storage():
    """
    Run storage server

    :rtype: None
    """

    os.system("python code/storage/storage.py")


if __name__ == '__main__':
    main()
