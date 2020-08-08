import discord
from discord.ext import commands

from utils import blacklist_data, rating_data, sommelier_data, stats_data

class Utility(commands.Cog):

    def __init__(self, client):

        self.client = client

        self.blacklistLog = 740422397869424672
        self.blacklistLogObj = None

    @commands.command()
    async def rules(self, ctx):

        embedToSend = discord.Embed(colour = discord.Colour.blurple())
        embedToSend.add_field(name = 'Ordering Rules', value = """**
        • No COFFEE
        • No spammy orders (For example: "tea grsogharihgasuhgosdhgosdg")
        • No NSFW Teas
        • No Offensive Teas (Hitler/Nazi, Sexism, and/or any other forms of Racism - Communism excluded)
        • No Drugs, Medications or Poisons
        • No Human or Animal Body Parts
        • Orders cannot contain people's names
        • Orders cannot contain text formatting or non-Latin characters, except numbers and !#$%&<>?".
        • Orders cannot contain links.
        • Must Include Tea
        Please respect these rules. Breaking any of them repeatedly will result in being blacklisted from the bot and/or banned from this server.**
        """)

        await ctx.send(embed = embedToSend)

    @commands.command()
    async def invite(self, ctx):

        embedToSend = discord.Embed(colour = discord.Colour.blurple())
        embedToSend.add_field(name = 'Useful Links', value = '[Invite me to your server!](https://discord.com/oauth2/authorize?client_id=507004433226268699&permissions=388161&scope=bot)\n[Join my support server](https://discord.gg/mP8U9ey)')

        await ctx.send(embed = embedToSend)

    @commands.command()
    async def stats(self, ctx):
        embedToSend = discord.Embed(colour = discord.Colour.blurple())

        statsDB = stats_data.GetData()

        embedToSend.add_field(name = 'Discord Tea Stats', value = """
        - **Orders Placed:** ``{}``
        - **Teas Delivered:** ``{}``
        - **Orders Declined/Cancelled:** ``{}``
        - **Quickorders Brewed:** ``{}``
        - **Ratings Given:** ``{}``
        - **Feedback Comments Given:** ``{}``
        - **Facts Told:** ``{}``
        - **Times it's been tea time:** ``{}``
        - **Times help command has been used:** ``{}``
        - **Times bot has logged on:** ``{}``
        """.format(
            statsDB['placed'],
            statsDB['delivered'],
            statsDB['declined'],
            statsDB['quickorders'],
            statsDB['ratings'],
            statsDB['feedback'],
            statsDB['facts'],
            statsDB['teatime'],
            statsDB['help'],
            statsDB['login']
        ))

        await ctx.send(embed = embedToSend)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(":ping_pong: | {}ms".format(round(self.client.latency * 1000)))

    @commands.command()
    async def approval(self, ctx):
        average = rating_data.GetAverage()
        await ctx.send('**Our average rating is {}:star:**'.format(round(average, 2)))

    @commands.command()
    async def blacklist(self, ctx, mode = None, user: discord.User = None):

        if self.blacklistLogObj is None:
            self.blacklistLogObj = ctx.guild.get_channel(self.blacklistLog)

        if mode is None:
            await ctx.send(':x: **| Incorrect usage.\nExamples:\n``tea!blacklist add @Lumiobyte``\n``tea!blacklist remove 368860954227900416``**')
            return

        if user is None:
            await ctx.send(':x: **| Please provide a user to blacklist.\nExamples:\n``tea!blacklist add @Lumiobyte``\n``tea!blacklist remove 368860954227900416``**')
            return

        if not sommelier_data.Check(ctx.author.id):
            await ctx.send(':lock: **| Only Tea Sommeliers can use this command!**')
            return

        if mode.lower() == 'add':
            blacklist_data.Add(user.id)

            await ctx.send(':white_check_mark: **| Blacklisted ``{}``.**'.format(user))
            await self.blacklistLogObj.send(':triangular_flag_on_post: **| ``{}`` has been blacklisted by ``{}``.**'.format(user, ctx.author))

        elif mode.lower() == 'remove':
            result = blacklist_data.Remove(user.id)

            if result == False:
                await ctx.send(':x: **| That user is not currently blacklisted.**')
                return

            await ctx.send(':white_check_mark: **| Removed ``{}`` from the blacklist.**'.format(user))
            await self.blacklistLogObj.send(':radio_button: **| ``{}`` was removed from the blacklist by ``{}``.**'.format(user, ctx.author))

        else:
            await ctx.send(':x: **| Incorrect usage.\nExamples:\n``tea!blacklist add @Lumiobyte``\n``tea!blacklist remove 368860954227900416``**')


def setup(client):
    client.add_cog(Utility(client))