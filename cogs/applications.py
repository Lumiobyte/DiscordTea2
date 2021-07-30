import discord
from discord.ext import commands

import random
import asyncio
from utils import sommelier_data

class Applications(commands.Cog):
    
    def __init__(self, client):

        self.client = client

        self.testOptions = [
            "Poggers tea",
            "Sloth drinking a tea",
            "Spicy tea: make red tea with fire and spices inside it",
            "Wumpus tea: wumpus with tea stacked on his head",
            "Sushi tea: have sushi being picked out of a tea cup with chopsticks",
            "Cereal tea: milk being poured into a tea cup and cereal inside",
            "TEA TIME! Tea that's a clock indicating it's tea time",
            "I dropped my phone in my tea! Have a damaged phone inside a tea cup"
        ]

        self.applicantRoleID = 744817921355808788

    @commands.command()
    async def apply(self, ctx):

        if ctx.guild.id != 524024216463605770:
            await ctx.send(":lock: **| That command cannot be used in this server.**")
            return

        if sommelier_data.Check(ctx.author.id):
            await ctx.send(":no_entry_sign: **| You're already a Tea Sommelier!**")
            return

        message = "To apply for Tea Sommelier, please check out <#803061995762745414> and then use tea!test in <#744842642302435368> and follow the instructions."

        await ctx.author.add_roles(ctx.guild.get_role(self.applicantRoleID))

        try:
            await ctx.author.send(message)
        except:
            await ctx.guild.get_channel(744842642302435368).send(ctx.author.mention + "\n" + message)

    @commands.command()
    @commands.has_role(744817921355808788)
    async def test(self, ctx):

        if ctx.channel.id != 744842642302435368:
            await ctx.send(":lock: **| That command cannot be used in this channel.**")
            return

        if sommelier_data.Check(ctx.author.id):
            await ctx.send(":no_entry_sign: **| You're already a Tea Sommelier!**")
            return

        await ctx.send(f":tea: Your test order is: **{random.choice(self.testOptions)}**\n\n*Edit an image to match the prompt to demonstrate your editing skills as they are required as a Tea Sommelier. Once you're finished, ping @Test Approver*")
        
    @commands.command()
    @commands.has_role(744817921355808788)
    async def stoptest(self, ctx):

        if ctx.channel.id != 744842642302435368:
            await ctx.send(":lock: **| That command cannot be used in this channel.**")
            return

        if sommelier_data.Check(ctx.author.id):
            await ctx.send(":no_entry_sign: **| You're already a Tea Sommelier!**")
            return

        try:
            await ctx.author.send(":white_check_mark: **| Ended your test.**")
        except:
            await ctx.send(":white_check_mark: **| Ended your test.**")
            await asyncio.sleep(2)

        await ctx.author.remove_roles(ctx.guild.get_role(744817921355808788))

    @commands.command()
    @commands.has_role(744817921355808788)
    async def finish(self, ctx):

        await ctx.message.delete()

        if ctx.guild.id != 524024216463605770:
            await ctx.send(":lock: **| That command cannot be used in this server.**")
            return

        if not sommelier_data.Check(ctx.author.id):
            await ctx.send(":no_entry_sign: **| You're not a Tea Sommelier!**")
            return 

        await ctx.author.remove_roles(ctx.guild.get_role(744817921355808788))

def setup(client):
    client.add_cog(Applications(client))