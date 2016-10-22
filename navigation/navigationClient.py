import tkinter as tk
import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("Socket established")

host = '127.0.0.1'
port = 8800

s.connect((host,port))
print("s.connect() complete")

def socket_send_data(data):
    s.sendall(str.encode(data))

def socket_send_info(x, y, theta):
    socket_send_data("%f %f %f"%(x, y, theta))

if __name__ == "__main__":
    while True:
        ipt = input("Please enter some input: ")
        socket_send_data(ipt)
