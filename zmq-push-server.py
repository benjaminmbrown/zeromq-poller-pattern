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
		topic = random.randrange(8,10)
		messagedata = "server#%s" % (topic, messagedata)
		print "%s %s" % (topic, messagedata)
		socket.send("%d %s" % (topic, messagedata))
		time.sleep(1)

def worker(port_push, port_sub):
	context = zmq.Context()
	socket_pull = context.socket(zmq.PULL)
	socket_pull.connect("tcp://localhost:%s" % port_push)

	print "Connected to server with port %s" % port_push

	socket_sub = context.socket(zmq.SUB)
	socket_sub = connect("tcp://localhost:%s" %port_sub)
	socket_sub.setsockopt(zmq.SUBSCRIBE, "9") #only subscribe to 9 topics

	#setup zmq poller to poll for messages on the socket connection to both
	#command server and publsher

	poller = zmq.Poller()
	poller.register(socket_pull, zmq.POLLIN)
	poller.register(socket_sub, zmq.POLLIN)

	#now we are doing work
	sould_continue = True
	while should_continue:
		socks = dict(poller.poll())
		if socket_pull in socks and socks[socket_pull] == zmq.POLLIN:
			message = socket_pull.recv()
			print "Received a control command : %s" % message
			if message == "Exit":
				print "Got an exit command, client will stop receiving messages"
				should_continue = False

		if socket_sub in socks and socks[socket_sub] == zmq.POLLIN:
			string = socket_sub.recv()
			topic,messagedata = string.split()
			print "Processing ... ", topic, messagedata

if __name__ == "__main__":
	#run a few servers
	server_push_port = "5556"
	server_pub_port = "5558"

	Process(target=push_server, args=(server_push_port,)).start()
	Process(target=publishing_server, args=(server_pub_port,)).start()
	Process(target=client, args=(server_push_port,server_pub_port,)).start()


