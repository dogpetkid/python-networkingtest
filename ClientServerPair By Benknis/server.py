##I take no credit
##Source: https://gist.github.com/Benknis/5647884

#!/usr/bin/env python
import socket, time
#things to begin with
def Tcp_connect( HostIp, Port ):
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HostIp, Port))
    return
    
def Tcp_server_wait ( numofclientwait, port ):
	global s2
	s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	s2.bind(('',port)) 
	s2.listen(numofclientwait) 

def Tcp_server_next ( ):
		global s
		s = s2.accept()[0]
   
def Tcp_Write(D):
   s.send(D + '\r')
   return 
   
def Tcp_Read( ):
	a = ' '
	b = ''
	while a != '\r':
		a = s.recv(1)
		b = b + a
	return b

def Tcp_Close( ):
   s.close()
   return 

Tcp_server_wait ( 5, 17098 )
Tcp_server_next()
print (Tcp_Read())
Tcp_Write('hi')
print (Tcp_Read())
Tcp_Write('hi')
Tcp_Close()
