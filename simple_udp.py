#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   simple_udp.py
@Time    :   2018/11/29 00:07:00
@Author  :   huanggang 
@Version :   1.0
@Contact :   867454076@qq.com
@Desc    :   None
'''

# here put the import lib
import socket

target_host="127.0.0.1"
target_port=80

client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

client.sendto("AAABBBCCC",(target_host,target_port))

data,addr=client.recvfrom(4096)

print(data)