import json

filepath = './database/sommelierStatsDB.json'

def CheckIfExists(userid):
    with open(filepath, encoding="utf-8", mode="r") as f:
        db = json.load(f)

        try:
            db[str(userid)]
        except:
            return False

def ClearStats():
    with open(filepath, encoding="utf-8", mode="r") as f:
        db = json.load(f)

        for userid in db:
            db[userid]['totalDeliveredWeek'] = 0
            db[userid]['totalDeclinedWeek'] = 0
            db[userid]['totalRatings'] = 0
            db[userid]['ratings'] = [0, 0, 1, 0, 0]

    with open(filepath, encoding="utf-8", mode="w") as f:
        json.dump(db, f)

def AddSommelier(userid):
    with open(filepath, encoding="utf-8", mode="r") as f:
        db = json.load(f)

        if CheckIfExists(userid) == True:
            return 

        userid = str(userid)

        db[userid] = {}
        db[userid]['totalDelivered'] = 0
        db[userid]['totalDeliveredWeek'] = 0
        db[userid]['totalDeclined'] = 0
        db[userid]['totalDeclinedWeek'] = 0
        db[userid]['totalRatings'] = 0
        db[userid]['ratings'] = [0, 0, 1, 0, 0]
        db[userid]['recentDelivered'] = ['Nothing here!', 'Nothing here!', 'Nothing here!']
        db[userid]['recentRatings'] = [3, 3, 3]

    with open(filepath, encoding="utf-8", mode="w") as f:
        json.dump(db, f)

def RemoveSommelier(userid):
    with open(filepath, encoding="utf-8", mode="r") as f:
        db = json.load(f)

        userid = str(userid)

        try:
            db.pop(userid)
        except:
            return False

    with open(filepath, encoding="utf-8", mode="w") as f:
        json.dump(db, f)

def AddOrderDelivered(userid):
    with open(filepath, encoding="utf-8", mode="r") as f:
        db = json.load(f)

        if CheckIfExists(userid) == False:
            AddSommelier(userid)
            return False

        userid = str(userid)

        db[userid]['totalDelivered'] += 1
        db[userid]['totalDeliveredWeek'] += 1

    with open(filepath, encoding="utf-8", mode="w") as f:
        json.dump(db, f)

def AddOrderDeclined(userid):
    with open(filepath, encoding="utf-8", mode="r") as f:
        db = json.load(f)

        if CheckIfExists(userid) == False:
            AddSommelier(userid)
            return False

        userid = str(userid)

        db[userid]['totalDeclined'] += 1
        db[userid]['totalDeclinedWeek'] += 1

    with open(filepath, encoding="utf-8", mode="w") as f:
        json.dump(db, f)

def AddRating(userid, rating):
    with open(filepath, encoding="utf-8", mode="r") as f:
        db = json.load(f)

        if CheckIfExists(userid) == False:
            AddSommelier(userid)
            return False

        userid = str(userid)

        db[userid]['totalRatings'] += 1
        db[userid]['ratings'][rating - 1] += 1
        db[userid]['recentRatings'].pop(0)
        db[userid]['recentRatings'].append(rating)

    with open(filepath, encoding="utf-8", mode="w") as f:
        json.dump(db, f)

def AddRecentDeliver(userid, order):
    with open(filepath, encoding="utf-8", mode="r") as f:
        db = json.load(f)

        if CheckIfExists(userid) == False:
            AddSommelier(userid)
            return False

        userid = str(userid)

        db[userid]['recentDelivered'].pop(0)
        db[userid]['recentDelivered'].append(order)

    with open(filepath, encoding="utf-8", mode="w") as f:
        json.dump(db, f)

def GetSommelier(userid):
    with open(filepath, encoding="utf-8", mode="r") as f:
        db = json.load(f)

        if CheckIfExists(userid) == False:
            AddSommelier(userid)
            return False

        userid = str(userid)

        return db[userid]