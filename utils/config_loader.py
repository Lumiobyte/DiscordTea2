import json

filepath = './database/config.json'

def GrabToken(token):
    with open(filepath, encoding="utf-8", mode="r") as f:
        db = json.load(f)

        return db[token]

