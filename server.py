from websocket import Server
import atexit

def quit():
    ws.close_ip(ip)
    ws.close()

print("Сервер")

ws = Server()
ws.start()
ip = ws.connect()

atexit.register(quit)

name = input("Ваше имя: ")
fname = input("Введите имя друга: ")

while True:
    message = input(f"{name}: ")
    if message != "":
        ws.send(ip, message)
    print(f"{fname}: " + ws.response(ip))
