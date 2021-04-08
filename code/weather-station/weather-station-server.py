from socket import socket, AF_INET, SOCK_DGRAM
from time import sleep
from station import StationSimulator

# Start the station
station_1 = StationSimulator(simulation_interval=1)

# Network socket
sock = socket(AF_INET, SOCK_DGRAM)


def start_client():
    """
    Starts the weather station for weather collection

    :rtype: None
    """
    station_1.turn_on()


def collect_weather_station_data():
    """
    Collects the data generated from the weather station over the past 72 hours.

    :rtype: None
    """

    # Capture data for 72 hours
    # Note that the simulation interval is 0.06 second

    # Two lists for temperature and precipitation
    temperature = []
    precipitation = []

    for _ in range(72):
        # Read new weather data and append it to the
        # corresponding list
        sleep(0.06)  # Accuracy and variance of data corresponds to how high sleep value is
        temperature.append(station_1.temperature)

        precipitation.append(station_1.rain)

    # Sends the data collected over to storage
    send_weather_to_storage(temperature, precipitation)


def send_weather_to_storage(temperature, precipitation):
    """
    Sends the temperature and the precipitation collected over the past 72 hours over to storage

    :rtype: None
    """

    # Converts the temperature and precipitation lists to string and adds them after each other
    rawData = str(temperature) + str(precipitation)

    # Converts the rawData to Bytes and sends it over to storage
    sock.sendto(rawData.encode(), ("localhost", 5555))


def main():
    """
    Starts the weather generation client and then constantly sends the generated data over to storage

    :rtype: None
    """

    # Starts the weather station for data generation
    start_client()

    # Constantly send data from weather station to server
    while True:
        collect_weather_station_data()

        # delay for 1 second until next data collection
        sleep(1)


if __name__ == '__main__':
    main()
