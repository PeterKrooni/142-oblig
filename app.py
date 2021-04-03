from time import sleep

import matplotlib.pyplot as plt
import ast
from io import BytesIO
from flask import Flask, render_template, send_file, redirect, url_for, request
from socket import socket

app = Flask(__name__)

sock = socket()

# Every data reading received from storage
storage_log = []

# Update interval for getting data from client
interval = 1


def init_socket():
    server_address = ("localhost", 5556)
    sock.connect(server_address)


@app.route('/')
def hello_world():
    return render_template('index.html', update_interval=interval)


@app.route('/', methods=['POST', 'GET'])
def handle_request():
    sentence = "give all"
    sock.send(sentence.encode())

    update_all_readings()
    print ("Readings updated.")
    all_plot()
    print ("Plotted all.")
    main_plot()
    print ("Plotted main.")

    # Return new page (currently only updating image so have to return new html site)
    return hello_world()


@app.route('/main.png')
def main_plot():
    """The view for rendering the scatter chart"""
    img = get_main_image()
    return send_file(img, mimetype='image/png', cache_timeout=0)


@app.route('/all.png')
def all_plot():
    img = get_all_image()
    return send_file(img, mimetype='image/png', cache_timeout=0)


def update_all_readings():
    # Clear all storage data
    storage_log.clear()

    # Get temperature and precipitation data (big buffer size to handle a long list of data)
    raw_data = sock.recv(1000000).decode()

    while raw_data.find(']') > -1:  # find returns -1 when arg not found
        # Get all items in temperature list
        temperature_data = ast.literal_eval(raw_data[:raw_data.index(']') + 1])
        raw_data = raw_data[raw_data.index(']') + 1:]

        # Get all items in precipitation list
        precipitation_data = ast.literal_eval(raw_data[:raw_data.index(']') + 1])
        raw_data = raw_data[raw_data.index(']') + 1:]

        # Convert all string data to float
        temperature_float = [float(i) for i in temperature_data]
        precipitation_float = [float(i) for i in precipitation_data]

        storage_log.append((temperature_float, precipitation_float))

    print ("readings updated.")
    print(storage_log)


def get_main_image():
    if len (storage_log) > 0:
        plt.plot(storage_log[len(storage_log)-1][0], color='red')    # temp
        plt.plot(storage_log[len(storage_log)-1][1], color='blue')   # prec

    plt.title('Temperature and precipitation for next 72 hours')
    plt.xlabel('Precipitation (blue), temperature (red)')

    # Save plot as image
    img = BytesIO()
    plt.savefig(img)
    img.seek(0)
    # Clear graphs from plot
    plt.clf()
    return img


def get_all_image():
    if len (storage_log) > 0:
        # Storage log has a list of tuples containing (72 hours of temp, 72 hours of precipitation)
        # First items in storage log, temperature
        plt.plot([x[0] for x in storage_log], color='red')
        # Second items in storage log, precipitation
        plt.plot([x[1] for x in storage_log])

    plt.title('Temperature and precipitation for all hours')
    plt.xlabel('Precipitation (blue), temperature (red)')

    img = BytesIO()
    plt.savefig(img)
    img.seek(0)
    # Clear graphs from plot
    plt.clf()
    return img


def main():
    init_socket()
    app.run()


if __name__ == '__main__':
    main()

main()
