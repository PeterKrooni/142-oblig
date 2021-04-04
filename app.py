import os
import threading
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
    graph_plot()

    # Return new page (currently only updating image so have to return new html site)
    return hello_world()


@app.route('/graph.png')
def graph_plot():
    img = get_plot()
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
    print ("Client readings updated from storage.")


def get_plot():
    plt.clf()
    fig, (ax_72, ax_all) = plt.subplots(nrows=2)
    fig.tight_layout(pad=5.0)
    fig.set_figheight(8)
    fig.set_figwidth(16)
    get_72(ax_72)
    get_all(ax_all)
    img = BytesIO()
    plt.savefig(img)
    img.seek(0)
    return img


def get_72(ax_72):
    if len (storage_log) > 0:
        ax_72.plot(storage_log[len(storage_log)-1][0], color='red')    # temp
        ax_72.plot(storage_log[len(storage_log)-1][1], color='blue')   # prec
    ax_72.set_ylabel('Temp(C), Prec (mm)')
    ax_72.set_xlabel('Time (hours)')
    ax_72.set_title('Precipitation (blue), Temperature (red) (72 hours)')


def get_all(ax_all):
    tempList = [x[0] for x in storage_log]
    temp_list = []
    for i in tempList:
        temp_list = temp_list+i

    precList = [x[1] for x in storage_log]
    prec_list = []
    for i in precList:
        prec_list = prec_list+i

    if len (storage_log) > 0:
        # Storage log has a list of tuples containing (72 hours of temp, 72 hours of precipitation)
        # First items in storage log, temperature
        ax_all.plot(temp_list, color='red')
        # Second items in storage log, precipitation
        ax_all.plot(prec_list, color='blue')
    ax_all.set_ylabel('Temp(C), Prec (mm)')
    ax_all.set_xlabel('Time (hours)')
    ax_all.set_title('Precipitation (blue), Temperature (red) (All time)')


def main():
    """
    Magic sleep numbers to make it seem like it's a complicated and sophisticated system
    """
    print("Starting storage and weather services...")
    ws = threading.Thread(target=run_weather_station)
    s = threading.Thread(target=run_storage)
    ws.start()
    s.start()
    sleep(1.2)
    print("> \t Weather station ready.")
    sleep(1.1)
    print("> \t Storage server ready.")
    sleep(0.5)
    print("Starting client TCP connection to server...")
    sleep(0.9)
    init_socket()
    print("> \t Connection ready.")
    sleep(0.7)
    print("Running flask app. Open your web browser and enter http://localhost:5000/")
    sleep(0.4)
    print("-----------------------------------READY--------------------------------")
    app.run()


def run_weather_station():
    os.system("python code/weather-station/weather-station-server.py")


def run_storage():
    os.system("python code/storage/storage.py")


if __name__ == '__main__':
    main()

main()
