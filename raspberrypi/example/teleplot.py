import socket
import math
import time

teleplotAddr = ("10.0.0.16",47269)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def sendTelemetry(name, value):
	now = time.time() * 1000
	msg = name+":"+str(now)+":"+str(value)
	sock.sendto(msg.encode(), teleplotAddr)

#https://github.com/nesnes/teleplot

i=0
while i < 1000:
	
	sendTelemetry("sin", math.sin(i))
	sendTelemetry("cos", math.cos(i))

	i+=0.1
	time.sleep(0.01)