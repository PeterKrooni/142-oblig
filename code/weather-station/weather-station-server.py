from socket import socket, AF_INET, SOCK_DGRAM
from time import sleep
from station import StationSimulator

# Start the station
station_1 = StationSimulator(simulation_interval=1)


# Network socket
sock = socket(AF_INET, SOCK_DGRAM)


def startClient():
    station_1.turn_on()


def getWeatherStationData():
    # Capture data for 72 hours
    # Note that the simulation interval is 1 second

    # Two lists for temperature and precipitation
    temperature = []
    precipitation = []

    for _ in range(72):
        # Read new weather data and append it to the
        # corresponding list
        sleep(0.2)
        temperature.append(station_1.temperature)

        precipitation.append(station_1.rain)

    sendWeatherToStorage(temperature,precipitation)


def sendWeatherToStorage(temperature, precipitation):

    rawData = str(temperature)+str(precipitation)
    sock.sendto(rawData.encode(), ("localhost", 5555))
    print (rawData)
    print("reeeeeeeeeeeeeeeee")


def main():
    startClient()
    # Constantly send data from weather station to server
    while True:
        getWeatherStationData()
        # delay for 5 seconds until next data collection
        sleep(1)

if __name__ == '__main__':
    main()