import matplotlib.pyplot as plt
import ast
from io import BytesIO
from flask import Flask, render_template, send_file, redirect, url_for, request
from socket import socket

app = Flask(__name__)

sock = socket()

# All temperature and precipitation readings
temperature = []
precipitation = []

# Update interval for getting data from client
interval = 1


def init_socket():
    server_address = ("localhost", 5556)
    sock.connect(server_address)
    sentence = "give last"
    sock.send(sentence.encode())


@app.route('/')
def hello_world():
    return render_template('index.html', update_interval=interval)


@app.route('/', methods=['POST', 'GET'])
def handle_request():
    # Send request to server
    sentence = "give last"
    sock.send(sentence.encode())

    # Clear station data
    temperature.clear()
    precipitation.clear()

    # Get temperature and precipitation data
    raw_data = (sock.recv(10000).decode())
    # Split at first ] occurrence (since its a string of a list)
    temperature_data = ast.literal_eval(raw_data[:raw_data.index(']') + 1])
    precipitation_data = ast.literal_eval(raw_data[raw_data.index(']') + 1:])

    # Convert all string data to float
    temperature_float = [float(i) for i in temperature_data]
    precipitation_float = [float(i) for i in precipitation_data]

    # Add float data to station data
    temperature.append(temperature_float)
    precipitation.append(precipitation_float)

    # Update plot
    main_plot()
    # Return new page (currently only updating image so have to return new html site)
    return hello_world()


@app.route('/main.png')
def main_plot():
    """The view for rendering the scatter chart"""
    img = get_main_image()
    return send_file(img, mimetype='image/png', cache_timeout=0)


def get_main_image():
    """Rendering the scatter chart"""
    # Clear graphs from lot
    plt.clf()

    # Print all plots if temperature is longer than 1, or just first if contains 1 element
    if len(temperature) > 1:
        for i in range(0, len(temperature) - 1):
            plt.plot(temperature[i], color='red')
    elif len(temperature) == 1:
        plt.plot(temperature[0], color='red')

    if len(precipitation) > 1:
        for i in range(0, len(precipitation) - 1):
            plt.plot(precipitation[i], color='blue')
    elif len(precipitation) == 1:
        plt.plot(precipitation[0], color='blue')

    plt.title('Temperature and precipitation for next 72 hours')
    plt.xlabel('Precipitation (blue), temperature (red)')

    # Save plot as image
    img = BytesIO()
    plt.savefig(img)
    img.seek(0)
    return img


def main():
    init_socket()
    app.run()


if __name__ == '__main__':
    main()

main()
