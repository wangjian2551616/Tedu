"""
基于select的socket复用  (和进程,线程的区别是:它是单线程程序 它只能处理IO任务,
更多情况下是配合进程线程一起使用)
"""
from socket import *
from select import select
from time import sleep

HOST = "0.0.0.0"
POST = 8888
ADDR = (HOST,POST)

s = socket()
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(ADDR)
s.listen(3)

s.setblocking(False)  # 将s套接字设置为非阻塞

rlist = [s]  #初始关注监听套接字
wlist = []
xlist = []

while True:
    # 循环监控IO的发生
    rs,ws,xs = select(rlist,wlist,xlist)
    for r in rs:  # 连接和发消息IO 分别加入监听列表
        if r == s:
            c,addr = r.accept()
            print("Connect from",addr)
            c.setblocking(False)  # c也设置非阻塞模式
            rlist.append(c)  # 把新的客户端套接字加入监控列表中
        else:
            data = r.recv(1024).decode()
            if not data:
                rlist.remove(r)  # 先把列表中监听套接字移除
                s.close()
                continue
            print(data)
            # r.send(b"OK")  # 这个发送操作是主动的 所以可以写进wlist中
            wlist.append(r)

    for w in ws:  # wlist 用的少 xlist Linux中用不到  别的操作系统用
        w.send(b"OK")  # 发送完一定要移除 否则会粘包
        wlist.remove(w)

