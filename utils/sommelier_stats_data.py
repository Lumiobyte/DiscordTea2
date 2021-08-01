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
        db[userid]['rank'] = 'new'
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

        totalDeliveredPrev = db[userid]['totalDelivered']
        db[userid]['totalDelivered'] += 1
        db[userid]['totalDeliveredWeek'] += 1

    with open(filepath, encoding="utf-8", mode="w") as f:
        json.dump(db, f)

    if (totalDeliveredPrev == 9 and db[userid]['totalDelivered'] == 10) or (totalDeliveredPrev == 99 and db[userid]['totalDelivered'] == 100) or  (totalDeliveredPrev == 249 and db[userid]['totalDelivered'] == 250):
        result = UpgradeRank(userid)
        return result

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
            return [False]

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

def GetRank(userid):
    with open(filepath, encoding="utf-8", mode="r") as f:
        db = json.load(f)

        if CheckIfExists(userid) == False:
            AddSommelier(userid)
            return False

        userid = str(userid)

        return db[userid]['rank']


def UpgradeRank(userid):

    with open(filepath, encoding="utf-8", mode="r") as f:
        db = json.load(f)

        if CheckIfExists(userid) == False:
            AddSommelier(userid)
            return False

        userid = str(userid)

        oldRank = db[userid]['rank']

        if db[userid]['rank'] == 'new':
            db[userid]['rank'] = 'som'
        elif db[userid]['rank'] == 'som':
            db[userid]['rank'] = 'vet'
        elif db[userid]['rank'] == 'vet':
            db[userid]['rank'] = 'mas'

        newRank = db[userid]['rank']

    with open(filepath, encoding="utf-8", mode="w") as f:
        json.dump(db, f)

    return [True, newRank, oldRank]


def GetAll():
    with open(filepath, encoding="utf-8", mode="r") as f:
        db = json.load(f)

        return db

def FixDatabase():

    with open(filepath, encoding="utf-8", mode="r") as f:
        db = json.load(f)

        for userid in db:
            
            if db[userid]['totalDelivered'] < 10:
                db[userid]['rank'] = 'new'
            elif db[userid]['totalDelivered'] >= 10 and db[userid]['totalDelivered'] <= 99:
                db[userid]['rank'] = 'som'
            elif db[userid]['totalDelivered'] >= 100 and db[userid]['totalDelivered'] <= 249:
                db[userid]['rank'] = 'vet'
            else:
                db[userid]['rank'] = 'mas'

    with open(filepath, encoding="utf-8", mode="w") as f:
        json.dump(db, f)
