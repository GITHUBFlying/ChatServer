#!/usr/bin/env python   
# -*- coding:UTF-8 -*-  

import socket, select, string, sys
import json

#as a client
ServerHost='47.100.3.155'
ServerPort=5000

robotid={
	"id": "robot",
	"moi_id":  0,
	"type"  :  0
}

if __name__=="__main__":
	if(len(sys.argv) > 2) :
		print 'Usage : python telnet.py hostname port'
		ServerHost = sys.argv[1]
		ServerPort = int(sys.argv[2])
	
	#as client
	client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#client.settimeout(2)	
	try:
		#连接远程IP  登录
		client.connect((ServerHost,ServerPort))
		print "connnected to remote server"	
		jsondata=json.dumps(robotid)
		client.send(jsondata)
	except:
		print "unable to connect"
		sys.exit()
	while True:
		data=client.recv(4096)
		if not data:
			print '\nDisconnected from chat server'
			sys.exit()
		else:
			print data
		client.send("ok")
		except:
				client.close()
			
			
