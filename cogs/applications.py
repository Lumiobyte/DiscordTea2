import discord
from discord.abc import Messageable
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

        await ctx.message.delete()

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

        await ctx.message.delete()

        if ctx.channel.id != 744842642302435368:
            await ctx.send(":lock: **| That command cannot be used in this channel.**")
            return

        if sommelier_data.Check(ctx.author.id):
            await ctx.send(":no_entry_sign: **| You're already a Tea Sommelier!**")
            return

        await ctx.send(f":tea: {ctx.author.mention}, Your test order is:\n**{random.choice(self.testOptions)}**\n\n*Edit an image to match the prompt to demonstrate your editing skills as they are required as a Tea Sommelier. Once you're finished, ping @Test Approver*")
        
    @commands.command()
    @commands.has_role(744817921355808788)
    async def stoptest(self, ctx):

        await ctx.message.delete()

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

        await ctx.send(":white_check_mark: **| {} ended their test.**".format(ctx.author.mention))

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

        await ctx.send(":white_check_mark: **| {} finished their test.**".format(ctx.author.mention))

    @commands.command(aliases = ['canttype', 'notype', 'secretcommand', 'finishtest', 'secretcmd'])
    async def noperms(self, ctx, user: discord.User = None):

        embed = discord.Embed(colour = discord.Colour.red())
        embed.add_field(name = ":speech_balloon: If you can't type in the brewery channels...", value = "**...it means you haven't finished your Sommelier Test.**\n\n__**TO FINISH THE TEST**__\n 1. Read <#740408887446077440> **thoroughly** and find the secret command.\n2. Once you've found it, type it in <#744842642302435368>.\n\nNobody will tell you the command, you will need to find it yourself. Do not skim the text, you will miss it and make the process take longer. It also contains important information so you know what commands to use as Sommelier")

        userMention = ""

        if user:
            userMention = user.mention

        await ctx.send(content = userMention, embed = embed)

def setup(client):
    client.add_cog(Applications(client))