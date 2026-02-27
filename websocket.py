import socket
import time

class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, ip, port):
        self.s.connect((ip, port))

    def send(self, message):
        self.s.send(str(message).encode("utf-8"))

    def response(self):
        return self.s.recv(1024).decode("utf-8")

    def close(self):
        self.s.close()


class Server:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ips = {}

    def start(self):
        self.s.bind(("0.0.0.0", 63325))
        self.s.listen(1)

    def connect(self):
        conn, addr = self.s.accept()
        self.ips[addr] = conn
        return addr

    def send(self, ip, message):
        self.ips[ip].send(str(message).encode("utf-8"))

    def response(self, ip):
        return self.ips[ip].recv(1024).decode("utf-8")

    def close_ip(self, ip):
        self.ips[ip].close()
    
    def close(self):
        self.s.close()

if __name__ == "__main__":
    ws = Client()
    ws.connect("26.216.188.196", 5000)
    ws.send("hello")
    print(ws.response())
    ws.close()
    time.sleep(10)

