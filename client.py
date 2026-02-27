from websocket import Client
import atexit

def quit():
    ws.close()

print("Клиент")

ws = Client()
ws.connect(input("IPv4 друга: "), 63325)

atexit.register(quit)

name = input("Ваше имя: ")
fname = input("Введите имя друга: ")

while True:
    message = input(f"{name}: ")
    if message != "":
        ws.send(message)
    print(f"{fname}: " + ws.response())
