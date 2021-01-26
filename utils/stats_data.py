import json

filepath = './database/statsDB.json'

# Stats saved:
# Orders placed
# Teas Delivered
# Orders declined/cancelled
# Quickorders Brewed
# Ratings given
# Feedback comments given
# Facts told
# Times it's been tea time
# Times help command has been used
# Times bot has logged on
# Messages sent

def GetData():
    with open(filepath, encoding="utf-8", mode="r") as f:
        db = json.load(f)

        return db

def WriteSingle(stat):
    with open(filepath, encoding="utf-8", mode="r") as f:
        db = json.load(f)

        if stat not in ['placed', 'delivered', 'declined', 'quickorders', 'ratings', 'feedback', 'facts', 'teatime', 'help', 'login', 'messages']:
            return

        db[stat] += 1

    with open(filepath, encoding="utf-8", mode="w") as f:
        json.dump(db, f)

