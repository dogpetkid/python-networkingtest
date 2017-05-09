from clienttest import *
from servertest import *

HOSTself = socket.gethostbyname(socket.gethostname())
print("Ip: " + HOSTself)
PORT = 8089##int(input("Port: "))
HOSTother = '192.168.112.146'##input("Input the other Ip: ")

def finding():
    print("Finding")
    with hostme(HOSTself,PORT) as sock:
        while True:
            try:
                get = listen(sock.connection)
                print(get)
                break
            except Exception as e:
                input(str(e))

def sending():
    print("Sending")
    with clientme(HOSTother,PORT) as sock:
        while True:
            try:
                send = speak(sock.clientsocket, input("Send: "))
                break
            except Exception as e:
                input(str(e))

if bool(input("Type a letter to go host ")):
    '''connection = hostme(HOSTself,PORT)
    connection.sock = connection.serversocket'''
    
    while True:
        finding()
        sending()

else:
    '''connection = clientme(HOSTother,PORT)
    connection.sock = connection.clientsocket'''
    
    while True:
        sending()
        finding()
