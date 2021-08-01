import json

filepath = "./database/boosters.json"

def Remove(user):
    with open(filepath, encoding="utf-8", mode="r") as f:
        db = json.load(f)

        try:
            db['boosters'].remove(user)
        except:
            return False

    with open(filepath, encoding="utf-8", mode="w") as f:
        json.dump(db, f)

def Add(user):
    with open(filepath, encoding="utf-8", mode="r") as f:
        db = json.load(f)

        if Check(user):
            return

        db['boosters'].append(user)

    with open(filepath, encoding="utf-8", mode="w") as f:
        json.dump(db, f)

def Check(user):
    with open(filepath, encoding="utf-8", mode="r") as f:
        db = json.load(f)

        if user in db['boosters']:
            return True
        else:
            return False

def GetAll():
    with open(filepath, encoding="utf-8", mode="r") as f:
        db = json.load(f)

        return db['boosters']