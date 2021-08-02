import discord
from discord.ext import commands

import random, datetime

from utils import stats_data

class Fun(commands.Cog):

    def __init__(self, client):
        
        self.client = client

        self.previousTime = datetime.datetime.now()

        self.factsList = [
            'Iced tea was invented at the 1904 St. Louis World’s Fair by an Englishman named Richard Blechynden.',
            'Tea bags were invented in 1908 in the United States by Thomas Sullivan.'
            'This bot is made in discord.py!',
            'It is believed that tea was invented by Chinese emperor Shen Nung in 2737 B.C. when a leaf fell in to his hot water.',
            'Gingko is a tea the Chinese believe that improves your memory.',
            'The thermal energy in the hot water of the tea causes the flavor to be spreaded easier from the tea bag, that is why people serve tea hot.',
            'Black tea has half the amount of caffeine compared to coffee.',
            'Just like milk, a cup of tea helps strengthen your bones.',
            'An experienced tea picker can collect around 32 kgs of tea in one day, enough tea for 14,000 cups.',
            'White tea, green tea, oolong tea, and black tea can be converted to a thousand different varieties.',
            'Tea kills your appetite and therefore the perfect drink when you are dieting.',
            'Cholesterol can be regulated with tea and it is also good for the heart.',
            'Green tea can kill cancer cells.',
            'Tea helps fight cavities – no more scary dentist visits.',
            'The Boston tea party is greatly responsible for the coffee outbreak in America. Hopefully with time America rediscovers tea, and reclaims its lost tea culture.'
        ]

    @commands.command()
    async def time(self, ctx):

        await ctx.message.delete()

        if (self.previousTime - datetime.datetime.now()).seconds >= random.randrange(5000, 8000):
            await ctx.send(':alarm_clock: **| It\'s tea time!**')
            self.previousTime = datetime.datetime.now()
            stats_data.WriteSingle("teatime")
        else:
            await ctx.send(':clock1: **| It\'s not tea time.**')

         
    @commands.command()
    async def fact(self, ctx):

        await ctx.message.delete()

        await ctx.send(':tea: **Random Tea Fact!** {}'.format(random.choice(self.factsList)))

        stats_data.WriteSingle('facts')

    @commands.command()
    async def tea(self, ctx):

        await ctx.send(':tea:')

    @commands.command()
    async def elephant(self, ctx):

        elephantRole = await ctx.guild.create_role(name = 'Elephant')

        # im sick of deleting these roles from my server await ctx.author.add_roles(elephantRole)

        #for i in range(4):
            #await ctx.send(elephantRole.mention)

        for i in range(5):
            await ctx.author.send(':elephant:')

        await ctx.author.edit(nick = 'Elephant 🐘')

        await ctx.author.send('https://discord.gg/aeCrzsjMx5 :elephant:')

        #this is annoying lol await ctx.guild.edit(name = ctx.guild.name + ' 🐘')

        await ctx.send('elephant')

        if ctx.author.id == 416987805739122699:
            await ctx.send(f'{ctx.author.mention} tt dev loves you')



        



def setup(client):
    client.add_cog(Fun(client))