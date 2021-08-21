from flask import Flask
from threading import Thread

discordClient = None

app = Flask('')

@app.route('/')
def main():

    global discordClient

    #return f"Hello! {len(discordClient.guilds)} guilds, {round(discordClient.latency() * 1000, 2)}ms ping"
    return f"Hello! Client is {discordClient}"

def run():
    app.run(host = "0.0.0.0", port = 8062)

def StartServing(client):
    discordClient = client
    server = Thread(target = run)
    server.start()
