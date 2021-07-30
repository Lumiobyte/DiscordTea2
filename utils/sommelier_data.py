import json

filepath = './database/sommelierDB.json'

def Remove(user):
    with open(filepath, encoding="utf-8", mode="r") as f:
        db = json.load(f)

        try:
            db['sommeliers'].remove(user)
        except:
            return False

    with open(filepath, encoding="utf-8", mode="w") as f:
        json.dump(db, f)

def Add(user):
    with open(filepath, encoding="utf-8", mode="r") as f:
        db = json.load(f)

        if Check(user):
            return

        db['sommeliers'].append(user)

    with open(filepath, encoding="utf-8", mode="w") as f:
        json.dump(db, f)

def Check(user):
    with open(filepath, encoding="utf-8", mode="r") as f:
        db = json.load(f)

        if user in db['sommeliers']:
            return True
        else:
            return False

def Amount():
    with open(filepath, encoding="utf-8", mode="r") as f:
        db = json.load(f)

        return len(db['sommeliers'])

def GetAll():
    with open(filepath, encoding="utf-8", mode="r") as f:
        db = json.load(f)

        return db['sommeliers']