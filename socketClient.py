import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("Socket established")

host = '127.0.0.1'
port = 8800

s.connect((host,port))
print("s.connect() complete")

while True:
    data = input("Please enter data: ")
    s.sendall(str.encode(data))
