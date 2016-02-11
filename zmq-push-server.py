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