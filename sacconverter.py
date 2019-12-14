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

l=[]
with open("vulnerables.txt", "r") as file:
    for x in file:
        l.append(x[:-1])
for i in l:
    sacfiles()
