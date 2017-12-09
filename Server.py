#!/usr/bin/env python   
# -*- coding:UTF-8 -*-  

import socket, select, string, sys
import json

#as a server
ListenerPort=5001
CONNECTION_LIST = []
RECV_BUFFER = 4096

robots=[]

def result(ip):
	res={
	"res":0,
	 "ip":ip
	}
	return json.dumps(res)

def handle_data(sock,ip,data):
	#print data
	res=json.loads(data)
	robotid=res['moi_id']
	if res['id'] == "user":
		print 'User:user connected,user want to connect robot:'+str(robotid)
		flag=True
		for robot in robots:
			if robotid == robot['moi_id']:
				print 'this robot is online!'
				sock.send(result(robot['ip']))
				flag=False
		if flag:
			#机器人未上线
			print "but this robot is offline"
			sock.send("{\"res\":1}")
	else:
		flag=True
		for robot in robots:
			if robotid == robot['moi_id']:
				print 'this robot has already resgistered'
				flag=False
		if flag:
			res[u'ip']=ip
			print 'robot id:'+str(robotid)+':resgistered'
			robots.append(res)
			sock.send("ok!")
	print 'Online robot-->:'
	for key in robots:
		print 'robotid:'+str(key['moi_id'])+" ip:"+key['ip']
	print '-----------------'
	
if __name__=="__main__":
	if(len(sys.argv) > 1) :
		ListenerPort = int(sys.argv[1])
	#as a server
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind(("0.0.0.0", ListenerPort))
	server_socket.listen(10)
	
	CONNECTION_LIST.append(server_socket)
	print "Chat server started on port " + str(ListenerPort)
			
	while True:
		try:
			read_list, write_list, error_list = select.select(CONNECTION_LIST , [], [],0.1)
			for sock in read_list:
				if sock==server_socket:
					# as server accept socket from robot
					sockfd, addr = server_socket.accept()
					CONNECTION_LIST.append(sockfd)
					#print "Client (%s, %s) connected" % addr
				else:
					#print data from robot
					#获取远程地址
					#try:
					#获取本地地址
					#print sock.getsockname()
					try:
						iip,iport=sock.getpeername()
						data=sock.recv(4096)
						handle_data(sock,iip,data)
					except Exception:
						print "Client (%s, %s) is offline" % (iip,iport)
						#print "Client offline"
						CONNECTION_LIST.remove(sock)
						'''
						for i in range(len(robots)):
							print robots[i]['ip']
							if robots[i]['ip']==iip:
								robots.pop(i)
						'''
		except:
				server_socket.close()
			
