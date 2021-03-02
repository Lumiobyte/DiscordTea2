import discord
from discord.ext import commands

from utils import rating_data, stats_data

class Feedback(commands.Cog):

    def __init__(self, client):
        self.client = client

        self.feedbackChannel = 740452826962198579
        self.feedbackChannelObj = None

        self.suggestionsChannel = 803911443635241010

    @commands.command()
    @commands.cooldown(1, 900, commands.BucketType.user)
    async def feedback(self, ctx, *, comment = None):

        if comment is None:
            await ctx.send(':x: **| Please give some feedback! Example: `tea!feedback The tea was tasty!`**')
            return

        if self.feedbackChannelObj is None:
            self.feedbackChannelObj = self.client.get_channel(self.feedbackChannel)

        await ctx.send(":white_check_mark: **| Your feedback has been sent. Thanks, {}! Remember you can always support us by `tea!vote` to help us grow!**".format(ctx.author.name))
        await self.feedbackChannelObj.send(":speech_left: **| Received feedback from `{}`: `{}`**".format(ctx.author, comment))

        stats_data.WriteSingle('feedback')

    @commands.command()
    @commands.cooldown(1, 900, commands.BucketType.user)
    async def suggest(self, ctx, *, suggestion = None):

        if suggestion is None:
            await ctx.send(':x: **| Please provide a suggestion.**')
            return

        if len(suggestion) >= 501:
            await ctx.send(':x: **| That\'s a bit too long. Keep it under 500 characters. Note that spamming or abusing suggestions will result in a blacklist.**')
            return

        await ctx.send(':white_check_mark: **| Suggestion sent! Thank you for your feedback :grin:! Remember you can always support us by `tea!vote` to help us grow!**')
        
        embed = discord.Embed(colour = discord.Colour.gold())
        embed.add_field(name = 'New Suggestion', value = suggestion)
        embed.set_footer(text = 'Suggestion by {} / {}'.format(ctx.author, ctx.author.id))

        message = await self.client.get_channel(self.suggestionsChannel).send(embed = embed)

        await message.add_reaction('🔺')
        await message.add_reaction('🔻')

        stats_data.WriteSingle('suggestions')



def setup(client):
    client.add_cog(Feedback(client))
