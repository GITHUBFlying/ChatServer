#!/usr/bin/env python   
# -*- coding:UTF-8 -*-  

import socket, select, string, sys
import json

#as a client
ServerHost='47.100.3.155'
ServerPort=5000

#as a robotClient
RobotHost=None
RobotListenerPort=6001
CONNECTION_LIST = []
RECV_BUFFER = 4096

userid={
	"id": "user",
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
	#as server client
	client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.settimeout(2)
	#as a robot server
	robotClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
	
	try:
		#连接远程IP  登录
		client.connect((ServerHost,ServerPort))
		print "connnected to remote server"	
		jsondata=json.dumps(userid)
		client.send(jsondata)
		data=client.recv(4096)
		res=json.loads(data)
		if res['res']==0:
			print 'that robot is online IP is :'+res['ip']
			RobotHost=res['ip']
		else:
			print 'that robot is offline'
			sys.exit()
		
	except:
		print "unable to connect"
		
	
	CONNECTION_LIST.append(client)
	CONNECTION_LIST.append(sys.stdin)
	
	try:
		robotClient.connect((RobotHost,RobotListenerPort))
		print "Connected to Robot"
	except:
		print "unable to connect"
		sys.exit()
		
	CONNECTION_LIST.append(robotClient)	
	
	while True:
		read_list, write_list, error_list = select.select(CONNECTION_LIST , [], [],0.1)
		for sock in read_list:
			if sock==client:
				#as client recevie message from server
				data=sock.recv(4096)
				if not data:
					print '\nDisconnected from chat server'
					sys.exit()
				else:
					print 'From Server:'+data
					prompt()
			elif sock==robotClient:
				data=sock.recv(4096)
				if not data:
					print '\nDisconnected from chat server'
					sys.exit()
				else:
					print 'From Robot:'+data
					prompt()
			elif sock==sys.stdin:
				msg=sys.stdin.readline()
				jsondata=json.dumps(userid)
				robotClient.send(jsondata)
				prompt()
			else:
				# print data from robot
				print "error"
			
			
