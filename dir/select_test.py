"""
select方法示例
"""
from socket import *
from select import select
from time import sleep
# 套接字io
s = socket()
s.bind(("0.0.0.0",8888))
s.listen(3)
#读写io
f = open("test","w")

# 监控IO
print("监控IO:")
sleep(3)  # 设置3秒等待客户端链接
rs,ws,xs = select([s],[],[])
print(rs)
print(ws)
print(xs)
#监控IO:
# [<socket.socket fd=3, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 8888)>]
# []
# []