#Socket Client

from tkinter import *
import socket

print("everything is imported")

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("socket is established")
#the public ip
host = '127.0.0.1'
port=8800
s.connect((host,port))

print("s.connect done")

while True:
    data = input("Please enter some datas: ")
    s.sendall(str.encode(data))