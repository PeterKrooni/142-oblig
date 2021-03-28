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


def main():
    startClient()
    # Constantly send data from weather station to server
    while True:
        getWeatherStationData()
        sendWeatherStationData()

        # delay for 5 seconds until next data collection
        sleep(5)


def startClient():
    station_1.turn_on()


def getWeatherStationData():
    # Capture data for 72 hours
    # Note that the simulation interval is 1 second
    for _ in range(72):
        # Sleep for 1 second to wait for new weather data
        # to be simulated
        sleep(1)
        # Read new weather data and append it to the
        # corresponding list
        temperature.append(station_1.temperature)
        precipitation.append(station_1.rain)


def sendWeatherStationData():
    clientData = (temperature.encode(), precipitation.encode())
    stationOutData = clientData.encode()
    size = sock.sendto(stationOutData, ("localhost", 5555))
    print(f"Sent {size} bytes to storage")
