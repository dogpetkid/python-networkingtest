import socket
import servertest

Vnum = "0.2.1"
HOST = '192.168.112.146'
PORT = 8089

class clientme():
    def __init__(self,HOST,PORT):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) ##start
        print("Waiting...")
        for i in range(1,35): ##Wait for connection
            try:
                self.clientsocket.connect((HOST,PORT))
                ##goes to verifying
                fail = False
                break
            except:
                if i%6 == 0:
                    print(".."+("."*int(((i/6)%3)+1))) ##Rotates from 3 to 5 dots to show that it is trying to conect
                fail = True
                pass
        if fail: print("No connection...")
        
        if not(fail):
            print("Verifying...")
            global Vnum
            speak(self.clientsocket,Vnum)
            vcheck = int(servertest.listen(self.clientsocket)) ##Gets how correct the version is
            if vcheck == 0:
                input("Compatibility between server/client is not possible.")
                fail = True
            elif vcheck == 1:
                input("Compatibility between server/client is probable, no attempt to connect will be made.")
            elif vcheck == 2:
                input("Compatibility between server/client is possible.")
                fail = False
            elif vcheck == 3:
                print("No compatibility issues.")
                fail = False
            
        if fail:
            input("Error occured, terminating connection.")
            raise LostComs
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.clientsocket.close()

class LostComs(Exception):
    pass

def speak(clientsocket,send):
    while True:
        try:
            clientsocket.send(bytes(send, 'utf-8')) ##sends data as byte type
            break
        except: ##Keeps program from crashing if one side loses connection
            raise LostComs
    return(send)

def arraypackage(array): ##array (of strings) to string
    package = str(array.pop())
    while len(array)>0:
        package = str(array.pop()) + "$!#" + package
    return package

if __name__ == "__main__":
    connection = clientme(HOST, PORT)
    while True:
        try:
            send = speak(connection.clientsocket, input("Send: "))
        except Exception as e:
            input(str(e))
        if send == "stop":
            break
