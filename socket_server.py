
import socket
import time
import sys
 
HOST_IP = "192.168.12.1"
HOST_PORT = 7654
 
print("Starting socket: TCP...")
socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
print("TCP server listen @ %s:%d!" %(HOST_IP, HOST_PORT) )
host_addr = (HOST_IP, HOST_PORT)
socket_tcp.bind(host_addr)
socket_tcp.listen(1) 
 
while True:
    print ('waiting for connection...')
    socket_con, (client_ip, client_port) = socket_tcp.accept()
    print("Connection accepted from %s." %client_ip)
 
    socket_con.send("Welcome to RPi TCP server!")
    
    while True:
        data=socket_con.recv(1024)
        
        
        if data:
            print(data)
            f = open('/home/pi/aip-python-sdk/test.txt', 'a')
        
            f.write(data)
            f.close()
            socket_con.send(data)
            
 
socket_tcp.close()