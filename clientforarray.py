from clienttest import *

HOST = '192.168.112.146'
PORT = 8089

if __name__ == "__main__":
    connection = clientme(HOST, PORT)
    while True:
        in1 = input("In1: ")
        in2 = input("In2: ")
        send = in1 + "$!#" + in2
        try:
            send = speak(connection.clientsocket, send)
        except Exception as e:
            input(str(e))
        if send == "stop$!#stop":
            break
