import tkinter as tk
import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("Socket established")

host = '127.0.0.1'
port = 8800

s.connect((host,port))
print("s.connect() complete")

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.textbox = tk.Text(self, height=10, width=30, borderwidth=2)
        self.textbox.pack(pady="30")
        self.textbox.config(highlightbackground='black')

        self.send = tk.Button(self)
        self.send["text"] = "Send Data"
        self.send["command"] = self.send_data
        self.send.pack()

        self.quit = tk.Button(self, text="QUIT", fg="red", command=root.destroy)
        self.quit.pack()

    def send_data(self):
        data = self.textbox.get("1.0","end")
        s.sendall(str.encode(data))

root = tk.Tk()
root.resizable(width=False, height=False)
root.geometry('{}x{}'.format(400, 300))
app = Application(master=root)
app.mainloop()
