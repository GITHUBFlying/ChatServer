#!/usr/bin/env python   
# -*- coding:UTF-8 -*-  

import socket, select, string, sys
import json

#as a client
ServerHost='47.100.3.155'
ServerPort=5000

#as a server
ListenerPort=6001
CONNECTION_LIST = []
RECV_BUFFER = 4096

robotid={
	"id": "robot",
	"moi_id":  0,
	"type"  :  0
}

def prompt() :
	#sys.stdout.write('<You> ')
	sys.stdout.flush()
    
if __name__=="__main__":
	if(len(sys.argv) > 2) :
		print 'Usage : python telnet.py hostname port'
		ServerHost = sys.argv[1]
		ServerPort = int(sys.argv[2])
	
	#as client
	client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#client.settimeout(2)
	#as a server
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind(("0.0.0.0", ListenerPort))
	server_socket.listen(10)
	
	CONNECTION_LIST.append(server_socket)
	print "Chat server started on port " + str(ListenerPort)
	
	try:
		#连接远程IP  登录
		client.connect((ServerHost,ServerPort))
		print "connnected to remote server"	
		jsondata=json.dumps(robotid)
		client.send(jsondata)
	except:
		print "unable to connect"
		sys.exit()
	
	CONNECTION_LIST.append(client)
	CONNECTION_LIST.append(sys.stdin)
	
	while True:
		try:
			read_list, write_list, error_list = select.select(CONNECTION_LIST , [], [],0.1)
			for sock in read_list:
				if sock==client:
					#as client recevie message from server
					data=sock.recv(4096)
					if not data:
						print '\nDisconnected from chat server'
						sys.exit()
					else:
						sys.stdout.write(data)
						prompt()
				elif sock==server_socket:
					# as server accept socket from robot
					sockfd, addr = server_socket.accept()
					CONNECTION_LIST.append(sockfd)
					print "User (%s, %s) connected" % addr
				elif sock==sys.stdin:
					msg=sys.stdin.readline()
					jsondata=json.dumps(robotid)
					client.send(jsondata)
					prompt()
				else:
					# print data from user
					data=sock.recv(4096)
					print "From User:"+data
					sock.send("hello i am from robot")
		except:
				client.close()
				server_socket.close()
			
			
