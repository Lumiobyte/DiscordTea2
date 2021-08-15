import discord
from discord.ext import commands

from plugins import statspage
from utils import stats_data

class Site(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        
        print("StatsPage starting")
        statspage.StartServing(self.client)


def setup(client):
    client.add_cog(Site(client))