#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   tcp_server.py
@Time    :   2018/12/01 00:12:52
@Author  :   huanggang 
@Version :   1.0
@Contact :   867454076@qq.com
@Desc    :   None
'''

# here put the import lib
import socket
import threading

bind_host ="0.0.0.0"
bind_port=9999

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((bind_host,bind_port))

server.listen(5)

print("Listen on %s:%d" % (bind_host,bind_port))

def handle_client(client):
    requst = client.recv(4096)

    print("[*]received:%s" % requst)

    client.send("ACK")
    client.close()

while True:
    client,addr = server.accept()
    print("acceptd connection from:%s:%d" % (addr[0],addr[1]))
    client_handler=threading.Thread(target=handle_client,args=(client,))
    client_handler.start()