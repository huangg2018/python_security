#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   bhpnet.py
@Time    :   2018/12/01 00:32:50
@Author  :   huanggang 
@Version :   1.0
@Contact :   867454076@qq.com
@Desc    :   模拟netcat工具
'''

# here put the import lib
import socket
import sys
import threading
import getopt
import subprocess

#定义全局变量
listen             = False
command            = False
upload             = False
execute            = ""
target             = ""
upload_destination = ""
port               = 0

def usage():
    print("BHP Net Tool")
    print("")
    print("Usage:bhpnet.py -t target_host -p port")
    print("-l --listen              - listen on[host]:[port] for incoming connections")
    print("-e --execute=file_to_run - execute the given file upon receiving a connections")
    print("-c --command             - initialize a command shell")
    print("-u --upload=destination  - upon receiving connection upload a file and write to [destination]")
    print("")
    print("")
    print("Examples:")
    print("bhpnet.py -t 192.168.249.128 -p 5555 -c")
    print("bhpnet.py -t 192.168.249.128 -p 5555 -l -u=c:\\target.exe")
    print("bhpnet.py -t 192.168.249.128 -p 5555 -l -e=\"cat /etc/passwd\"")
    print("echo 'ABADSASFA'|./bhpnet.py -t 192.168.249.128 -p 5555")
    sys.exit(0)

def main():
    global listen
    global port
    global command
    global execute
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hle:t:p:cu:",
        ["help","listen","execute","target","port","command","upload"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o, a in opts:
        if o in ("-h","--help"):
            usage()
        if o in ("-l","--listen"):
            listen = True
        if o in ("-e","--execute"):
            execute= True
        if o in ("-t","--target"):
            target=a
        if o in ("-p","--port"):
            port=int(a)
        if o in ("-c","--command"):
            command=a
        if o in ("-u","--upload"):
            upload_destination=a
        else:
            assert False,"Unhandled Option"

#如果没有监听，那么当前模式为客户端模式
if not listen and len(target) and port>0:
    #从标准终端读取数据
    buffer = sys.stdin.read()
    #将数据发送到服务端
    client_sender(buffer)
#如果处于监听状态，那么当前处于服务端模式
if listen:
    server_loop()

#TCP客户端
def client_sender(buffer):
    #创建SOCKET套接字
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        #连接到TCP服务端
        client.connect((target,port))
        if len(buffer):
            client.send(buffer)
        while True:
            recv_len = 1
            response = ""

            #循环接收服务端返回的数据
            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response+= data
                #如果接收到的数据大小小于单次接收数据的大小，则说明数据已经接收完毕
                if recv_len < 4096:
                    break
            #打印完整的响应数据
            print(response)
            
            #等待更多的输入
            buffer = raw_input("")
            buffer+="\n"
            #发送出去
            client.send(buffer)


    except:
        print("[*]Exception! Exiting")
        #关闭连接
        client.close()
def raw_input(input):
    pass
    return input    
#TCP服务端
def server_loop():
    #创建SOCKET套接字
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #绑定IP和端口
    server.bind((target,port))
    #启动5个监听进程
    server.listen(5)

    #死循环,循环监听每个进程接收的数据
    while True:
        #接收客户端发来的请求
        client,addr = server.accept()
        #创建线程处理客户端发过来的请求
        client_thread = threading.Thread(target=handle_client,args=(client,))
        client_thread.start()

#处理来自客户端发起的文件上传,命令执行，shell命令
def handle_client(client_socket):
    global upload
    global execute
    global command

    #检查是否为文件上传
    if len(upload_destination):
        #读取文件的buffer
        file_buffer=""

        #从客户端持续读取数据,直到读取完用户需要上传的文件为止
        while True:
            data = client_socket.recv(4096)

            if not data:
                break
            else:
                file_buffer += data

        #将缓存文件写入上传目录
        try:
            file_descriptor = open(upload_destination,"wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()
            #告知客户端已经上传完毕
            client_socket.send(u"成功保存文件到:%s" % upload_destination)
        except IOError as err:
            client_socket.send(u"上传文件失败:%s" % str(err)) 

    #检查命令执行
    if len(execute):
        #运行命令
        output = run_command(execute)

def run_command(cmd):
    pass
    return ""   



