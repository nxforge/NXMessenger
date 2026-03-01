# 2026 NXFORGE nx.messenger v0.1 module data

import os
import json


def init() -> None:
    os.makedirs(nxpath("NXMessenger\\data"), exist_ok=True)


def abspath(path: str):
    return os.path.abspath(path)


def nxpath(path: str):
    return os.path.join(os.path.expanduser("~"), ".nx", path)


class DataBaseChats:
    def __init__(self):
        pass


    def add(self, data: dict) -> None:
        chats = self.load()
        for d in chats:
            if d == data:
                break
        else:
            chats.append(data)
        self.save(chats)

    
    def remove(self, index):
        chats = self.load()
        chats.remove(chats[index])
        self.save(chats)


    def clear(self) -> None:
        self.save(list())


    def load(self) -> list:
        path = nxpath("NXMessenger\\data\\chats.json")

        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    

    def save(self, data: list) -> None:
        path = nxpath("NXMessenger\\data\\chats.json")

        with open(path, "w") as f:
            json.dump(data, f)


if __name__ == "__main__":
    init()
    DataBaseChats().clear()
