import discord
from discord.ext import commands

from plugins import statspage
from utils import stats_data

class Site(commands.Cog):

    def __init__(self, client):
        self.client = client

        statspage.StartServing(self.client)


def setup(client):
    client.add_cog(Site(client))