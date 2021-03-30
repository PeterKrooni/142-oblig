from socket import socket, AF_INET, SOCK_DGRAM
from time import sleep
from station import StationSimulator

# Start the station
station_1 = StationSimulator(simulation_interval=1)

# Two lists for temperature and precipitation
temperature = []
precipitation = []

# Client data, contains temperature and precipitation
stationData = ([], [])

# Network socket
sock = socket(AF_INET, SOCK_DGRAM)


def startClient():
    station_1.turn_on()


def getWeatherStationData():
    # Capture data for 72 hours
    # Note that the simulation interval is 1 second

    for _ in range(72):
        # Sleep for 1 second to wait for new weather data
        # to be simulated

        sleep(0.1) #denne gjør at alt tar veldig lang tid

        # Read new weather data and append it to the
        # corresponding list
        temperature.append(station_1.temperature)

        precipitation.append(station_1.rain)

def sendWeatherInSmallChunks():
    for i in range(len(temperature)):
        print(f"tempWeatherStation:{temperature[i]}, precWeatherStation:{precipitation[i]}")
        sock.sendto(str((temperature[i])).encode(), ("localhost", 5555))
        sock.sendto(str((precipitation[i])).encode(), ("localhost", 5555))

    print("reeeeeeeeeeeeeeeee")


def main():
    startClient()
    # Constantly send data from weather station to server
    while True:
        getWeatherStationData()
        sock.sendto("ok".encode(), ("localhost", 5555)) #signal that the station is ready to send new info
        sendWeatherInSmallChunks()

        # delay for 5 seconds until next data collection
        sleep(5)

if __name__ == '__main__':
    main()