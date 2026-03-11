# 2026 NXFORGE nx.messenger v0.1

import requests

def post(ip: str, message: str):
    requests.post(f"http://{ip}", json={"message": message})

if __name__ == "__main__":
    post("192.168.0.106:63323", "Мыло")
