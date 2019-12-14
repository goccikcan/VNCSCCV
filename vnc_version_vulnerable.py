#VNC request deneme.

import socket

host="213.141.156.24"
port=5920
client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
client.send("data")
response=client.recv(4096)
print (response)
                     
