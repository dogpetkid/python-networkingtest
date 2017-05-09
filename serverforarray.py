from servertest import *

HOST = socket.gethostbyname(socket.gethostname())
PORT = 8089

connection = hostme(HOST,PORT)
while True:
    try:
        get = listen(connection.connection)
    except Exception as e:
        input(str(e))
    in1, in2 = get.split("$!#")
    try:
        in1 = int(in1)
        in2 = int(in2)
        print(in1+in2)
    except:
        print(in1)
        print(in2)
    if get == "stop$!#stop":
        break
