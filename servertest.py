import socket

Vnum = "1.0"
HOST = socket.gethostbyname(socket.gethostname())
PORT = 8089

class hostme():
    def __init__(self,HOST,PORT,timeout=600,num=1):
        print("Ip: " + str(HOST))
        print("Port: " + str(PORT))

        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) ##start
        self.serversocket.bind((HOST, PORT)) ##Bind address of ip,port
        self.serversocket.listen(num) #*num* connections max
        print("Listening...")
        if num == 1: ##for individual connections
            self.connection, self.address = self.serversocket.accept()
            self.connection.settimeout(timeout)
        else: ##for several connections
            self.connection = []
            self.adress = []
            for i in range(num):
                tempsock = self.serversocket.accept()
                connection.append(tempsock[0])
                adress.append(tempsock[1])
                self.connection[i].settimeout(timeout)
        print("Connected!")
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.serversocket.close()

class LostComs(Exception):
    input("Connection was lost.")

def listen(connection):
    while True:
        try:
            data = connection.recv(64) ##Receives data
            if connection.gettimeout() <= 0:
                raise LostComs
        except: ##Keeps program from crashing if one side loses connection
            raise LostComs
        if len(data) > 0: ##Checks if there is data
            data = data.decode('utf-8') ##Decodes data
            break
    return(data)

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
