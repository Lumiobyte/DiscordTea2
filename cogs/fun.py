import discord
from discord.ext import commands

import random

from utils import stats_data

class Fun(commands.Cog):

    def __init__(self, client):
        
        self.client = client

        self.factsList = [
            'Iced tea was invented at the 1904 St. Louis World’s Fair by an Englishman named Richard Blechynden.',
            'Tea bags were invented in 1908 in the United States by Thomas Sullivan.'
            'This bot is made in discord.py!',
            'It is believed that tea was invented by Chinese emperor Shen Nung in 2737 B.C. when a leaf fell in to his hot water.',
            'Mauna Kea is a whole island dedicated for tea plantation!',
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

        number = random.randint(1, 13)

        if number == 4:
            await ctx.send(":alarm_clock: **It's tea time!**")
            stats_data.WriteSingle('teatime')
        else:
            await ctx.send(":clock1: **It isn't tea time.**")

         
    @commands.command()
    async def fact(self, ctx):

        await ctx.message.delete()

        await ctx.send(':tea: **Random Tea Fact! {}'.format(random.choice(self.factList)))

        stats_data.WriteSingle('facts')



def setup(client):
    client.add_cog(Fun(client))