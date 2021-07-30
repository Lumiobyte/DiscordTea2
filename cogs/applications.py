import discord
from discord.ext import commands

import random
from utils import sommelier_data, sommelier_stats_data

class Applications(commands.Cog):
    
    def __init__(self, client):

        self.client = client

    @commands.command()
    async def apply(self, ctx):

        if sommelier_data.Check(ctx.author.id):
            await ctx.send(":no_entry_sign: **| You're already a Tea Sommelier!**")
            return