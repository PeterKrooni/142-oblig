import matplotlib.pyplot as plt
import threading
import ast
from time import sleep
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
    sentence = "give shit"
    sock.send(sentence.encode())

@app.route('/')
def hello_world():
    return render_template('index.html', update_interval=interval)


@app.route('/', methods=['POST', 'GET'])
def handle_request():
    temperature = []
    precipitation = []

    print("request recieved")
    temp = (sock.recv(1024).decode())
    temp1 = ast.literal_eval(temp[:temp.index(']')+1])
    prec1 = ast.literal_eval(temp[temp.index(']')+1:])
    print(temp1)
    print(prec1)

    temperature.append([float(i) for i in temp1])
    precipitation.append([float(i) for i in prec1])
    print(temperature)
    """
    list(filter(lambda k: '\'' in k, temp))
    li = list(temp.split(","))
    print(f"list: {li}")

    print(f"temp: {temp}")
    print(temp[10])
    print("temp updated")
"""


    prec = (sock.recv(1024).decode())
    for j in prec:
        precipitation.append(float(j))

    print(f"prec: {prec}")
    precipitation.append(prec)
    print("prec updated")

    main_plot()
    return hello_world()


@app.route('/main.png')
def main_plot():
    """The view for rendering the scatter chart"""
    img = get_main_image()
    return send_file(img, mimetype='image/png', cache_timeout=0)


def get_main_image():
    """Rendering the scatter chart"""
    plt.plot(temperature, color='red')
    plt.plot(precipitation, color='blue')
    plt.title('Look at this graph')
    plt.xlabel('Precipitation (blue), temperature (red)')

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
