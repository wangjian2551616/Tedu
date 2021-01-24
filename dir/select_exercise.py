"""
编写一个日志记录程序
编写一个服务端程序,同时监控多个客户端发送过来的错误信息,将其写入到一个日志文件中.
同时监控服务端的本地(终端)输入内容,也写入到日志中.
日志内容包含信息和时间,每条占一行.
"""
from socket import *
from select import select
from time import ctime
import sys

HOST = "0.0.0.0"
POST = 8888
ADDR = (HOST,POST)

s = socket()
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(ADDR)
s.listen(3)

# 打开日志
f = open("log.txt","a")

s.setblocking(False) # 将套接字设置为非阻塞

rlist = [s,sys.stdin]
wlist = []
xlist = []

while True:
    # 循环监控IO的发生
    rs,ws,xs = select(rlist,wlist,xlist)  # 监控
    for r in rs:  # 连接和发消息IO 分别加入监听列表
        if r == s:
            c,addr = r.accept()
            print("Connect form",addr)
            c.setblocking(False) # c 也设置监听非阻塞模式
            rlist.append(c)  # 把新的客户端套接字加入监听列表中
        elif r == sys.stdin:
            f.write("%s %s"%(ctime(),r.readline()))
            f.flush()  # 刷新文件缓冲
        else:
            data = r.recv(1024)
            if not data:
                rlist.remove(r)
                s.close()
                continue
            f.write("%s %s"%(ctime(),data.decode()))
            f.flush()



