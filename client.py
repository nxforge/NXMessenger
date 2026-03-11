# 2026 NXFORGE nx.messenger v0.1

import requests

def post(ip: str, message: str):
    requests.post(f"http://{ip}", json={"message": message})
