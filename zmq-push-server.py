import zmq
import time
import sys
import random
from multiprocessing import Process

def push_server(port="5556"):
	context = zmq.Context()
	socket = context.socket(zmq.PUSH)
	socket.bind("tcp://*:%s" % port)
	print "Running server on port : ", port

	for reqnum in range(100):
		if(reqnum<95):
			socket.send("Continue")
		else:
			socket.send("Exit")
			break
		time.sleep(1)

def publishing_server(port="5558"):
	
	context = zmq.Context()
	socket = context.socket(zmq.PUB)
	socket.bind("tcp://*:%s" % port)
	publisher_id = random.randrange(0,9999)

	for reqnum in range(100):
		topic = ranomd.randrange(8,10)
		messagedata = "server#%s" % (topic, messagedata)
		print "%s %s" % (topic, messagedata)
		socket.send("%d %s" % (topic, messagedata))
		time.sleep(1)