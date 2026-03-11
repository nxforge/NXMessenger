# 2026 NXFORGE nx.messenger v0.1

from flask import Flask, request, jsonify

app = Flask(__name__)
messages = list()


@app.route('/', methods=['POST'])
def handle_post():
    global messages

    data = request.json
    ip = request.remote_addr

    print(f"{ip}: {data}")

    messages.append({
        "ip": ip,
        "message": data["message"]
    })

    return jsonify({"status": 200, "ip": ip, "received": data})


def get_messages(ip: str):
    chat_messages = []
    for message in messages:
        if message["ip"] == ip.split(":")[0]:
            chat_messages.append(message["message"])
    return chat_messages


def run(port):
    app.run(host="0.0.0.0", port=port)
