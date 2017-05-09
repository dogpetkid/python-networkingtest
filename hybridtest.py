from clienttest import *
from servertest import *

HOSTself = socket.gethostbyname(socket.gethostname())
print("Ip: " + HOSTself)
PORT = int(input("Port: "))
HOSTother = input("Input the other Ip: ")

def finding():
    print("Finding")
    while True:
        try:
            get = listen(connection.sock)
            print(get)
            break
        except Exception as e:
            input(str(e))

def sending():
    print("Sending")
    while True:
        try:
            send = speak(connection.sock, input("Send: "))
            break
        except Exception as e:
            input(str(e))

if bool(input("Type a letter to go host ")):
    connection = hostme(HOSTself,PORT)
    connection.sock = connection.connection
    
    while True:
        finding()
        sending()

else:
    connection = clientme(HOSTother,PORT)
    connection.sock = connection.clientsocket
    
    while True:
        sending()
        finding()
