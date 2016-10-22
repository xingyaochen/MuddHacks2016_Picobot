import tkinter as tk
import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("Socket established")

host = '192.168.43.109'
port = 8800

def connect():
    s.connect((host,port))
    print("s.connect() complete")

connect()

def socket_send_data(data):
    try:
        s.sendall(str.encode(data))
    except BrokenPipeError:
        connect()

def socket_send_info(fnum, x, y, theta):
    socket_send_data("%08.8f:%08.8f:%08.8f:%08.8f#"%(fnum, x, y, theta))

if __name__ == "__main__":
    while True:
        ipt = input("Please enter some input: ")
        socket_send_data(ipt)
