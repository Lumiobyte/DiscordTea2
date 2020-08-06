import discord
from discord.ext import commands

from utils import rating_data

class Feedback(commands.Cog):

    def __init__(self, client):
        self.client = client

        self.ratingsChannel = 740452811287822398
        self.ratingsChannelObj = None

        self.feedbackChannel = 740452826962198579
        self.feedbackChannelObj = None

    @commands.command()
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def feedback(self, ctx, *, comment = None):
        feedback_log = discord.utils.get(self.client.get_all_channels(), id = self.feedbackChannel)

        if comment is None:
            await ctx.send(':x: **| Please give some feedback! Example: ``tea!feedback The tea was tasty!``**')
            return

        if self.feedbackChannelObj is None:
            self.feedbackChannelObj = ctx.guild.get_channel(self.feedbackChannel)

        await ctx.send(":white_check_mark: **| Your feedback has been sent. Thanks, {}!**".format(ctx.author.name))
        await feedback_log.send(":star: **| Received feedback from `{}`: `{}`**".format(ctx.author, comment))

    @commands.command()
    @commands.cooldown(1, 900, commands.BucketType.user)
    async def rate(self, ctx, rating = None):
        
        
        feedback_log = discord.utils.get(self.client.get_all_channels(), id = self.ratingsChannel)
        stars = ''

        if rating is None:
            await ctx.send(':x: **| Please give a rating between 1 and 5 stars, no decimals.**')
            return

        try:
            rating = int(rating)
        except:
            await ctx.send(":no_entry_sign: **| Your rating must be between 1 and 5 and cannot be a decimal!**")
            return

        if rating > 5 or rating < 1:
            await ctx.send(":no_entry_sign: **| Your rating must be between 1 and 5 and cannot be a decimal!**")
            return

        if self.ratingsChannelObj is None:
            self.ratingsChannelObj = ctx.guild.get_channel(self.ratingsChannel)

        rating_data.Add(rating)

        for i in range (0, rating):
            stars += ':star:'

        await ctx.send(":star: **| You rated this service {}! Thanks for your feedback!**".format(stars))

        await feedback_log.send(":star: **| Received rating from `{}`: {}**".format(ctx.author, stars))


def setup(client):
    client.add_cog(Feedback(client))