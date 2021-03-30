from socket import socket

def main():
    sock = socket()
    server_address = ("localhost", 5555)
    sock.connect(server_address)
    sentence = input("Input lowercase sentence: ")
    sock.send(sentence.encode())
    new_sentence = sock.recv(1024).decode()
    print(f"From Server: {new_sentence}")
    sock.close()

if __name__ == '__main__':
    main()