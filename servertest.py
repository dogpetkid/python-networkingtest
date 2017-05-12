import socket
import clienttest

Vnum = "0.2.1"
HOST = socket.gethostbyname(socket.gethostname())
PORT = 8089

class hostme():
    def __init__(self,HOST,PORT,num=5):
        print("Ip: " + str(HOST))
        print("Port: " + str(PORT))

        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) ##start
        self.serversocket.bind((HOST, PORT)) ##Bind address of ip,port
        self.serversocket.listen(num) #*num* connections max
        print("Listening...")
        self.connection, self.address = self.serversocket.accept() ##accepts connections
        fail = False
        
        print("Verifying...")
        clientVnum = listen(self.connection)
        clientVnum = clientVnum.split(".") ##Gets version of client
        global Vnum
        serverVnum = Vnum.split(".") ##Gets version of server
        vcheck = 0
        for n in range(3): ##Checks how far in the versions are the same
            if serverVnum[n] == clientVnum[n]:
                vcheck+=1
            else: break
        clienttest.speak(self.connection,str(vcheck))
        if vcheck == 0:
            input("Compatibility between server/client is not possible.")
            fail = True
        elif vcheck == 1:
            input("Compatibility between server/client is probable, no attempt to connect will be made.")
            fail = True
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
        self.serversocket.close()

class LostComs(Exception):
    pass

def listen(connection):
    while True:
        try:
            data = connection.recv(64) ##Receives data
        except: ##Keeps program from crashing if one side loses connection
            raise LostComs
        if len(data) > 0: ##Checks if there is data
            data = data.decode('utf-8') ##Decodes data
            break
    return(data)

def arrayunpackage(package): ##string to array (of strings)
    array = package.split("$!#")
    return array

if __name__ == "__main__":
    connection = hostme(HOST,PORT)
    while True:
        try:
            get = listen(connection.connection)
            print(get)
        except Exception as e:
            input(str(e))
        if get == "stop":
            break
