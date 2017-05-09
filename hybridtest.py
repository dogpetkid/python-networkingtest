from clienttest import *
from servertest import *

HOSTself = socket.gethostbyname(socket.gethostname())
print("Ip: " + HOSTself)
PORT = 8089##int(input("Port: "))
HOSTother = '10.72.20.78'##input("Input the other Ip: ")

def finding():
    print("Finding")
    if True:##with hostme(HOSTself,PORT) as sock:
        while True:
            try:
                get = listen(connection.sock)
                print(get)
                break
            except Exception as e:
                input(str(e))

def sending():
    print("Sending")
    if True:##with clientme(HOSTother,PORT) as sock:
        while True:
            try:
                send = speak(connection.sock, input("Send: "))
                break
            except Exception as e:
                input(str(e))

if bool(input("Type a letter to go host ")):
    connection = hostme(HOSTself,PORT)
    connection.sock = connection.serversocket
    
    while True:
        finding()
        sending()

else:
    connection = clientme(HOSTother,PORT)
    connection.sock = connection.clientsocket
    
    while True:
        sending()
        finding()
