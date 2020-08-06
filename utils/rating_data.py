import json

filepath = './database/ratingsDB.json'

def Add(rating):
    with open(filepath, encoding="utf-8", mode="r") as f:
        db = json.load(f)

        db[str(rating)] += 1

    with open(filepath, encoding="utf-8", mode="w") as f:
        json.dump(db, f)

def GetAverage():
    with open(filepath, encoding="utf-8", mode="r") as f:
        db = json.load(f)

        total = 0
        counter = 0

        for i in range(1, 6):
            for x in range(0, db[str(i)]):
                total += i
                counter += 1

        average = total / counter
        return average