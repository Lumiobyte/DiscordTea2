import discord
from discord.ext import commands

from utils import rating_data, stats_data

class Feedback(commands.Cog):

    def __init__(self, client):
        self.client = client

        self.feedbackChannel = 740452826962198579
        self.feedbackChannelObj = None

    @commands.command()
    @commands.cooldown(1, 900, commands.BucketType.user)
    async def feedback(self, ctx, *, comment = None):

        if comment is None:
            await ctx.send(':x: **| Please give some feedback! Example: ``tea!feedback The tea was tasty!``**')
            return

        if self.feedbackChannelObj is None:
            self.feedbackChannelObj = self.client.get_channel(self.feedbackChannel)

        await ctx.send(":white_check_mark: **| Your feedback has been sent. Thanks, {}! Remember you can always support us by ``tea!vote`` for us to help us grow!**".format(ctx.author.name))
        await self.feedbackChannelObj.send(":speech_left: **| Received feedback from `{}`: `{}`**".format(ctx.author, comment))

        stats_data.WriteSingle('feedback')


def setup(client):
    client.add_cog(Feedback(client))
