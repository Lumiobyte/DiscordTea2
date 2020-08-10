import discord
from discord.ext import commands

class Orders(commands.Cog):

    def __init__(self, client):

        self.client = client

        self.uses = 0

    @commands.command()
    async def order(self, ctx):

        await ctx.send('Hello, {}!\n\n**Discord Tea** is undergoing a large update, and will be ready for use in a few days. If you have any questions or would like to be notified when the update is released, please join our support server.\n\nhttps://discord.gg/wKgKzV8'.format(ctx.author.mention))

        self.uses += 1
        print(str(self.uses) + str(ctx.author))

    @commands.command()
    async def quickorder(self, ctx):

        await ctx.send('Hello, {}!\n\n**Discord Tea** is undergoing a large update, and will be ready for use in a few days. If you have any questions or would like to be notified when the update is released, please join our support server.\n\nhttps://discord.gg/wKgKzV8'.format(ctx.author.mention))

        self.uses += 1
        print(str(self.uses) + str(ctx.author))


def setup(client):
    client.add_cog(Orders(client))


