import discord
from discord.ext import commands

class Utility(commands.Cog):

    def __init__(self, client):

        self.client = client

        self.blacklistLog = 0
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
        embedToSend.add_field(name = 'Useful Links', value = '[Invite me to your server!](https://youtube.com)\n[Join my support server](https://discord.gg/wapper)')

        await ctx.send(embed = embedToSend)

    @commands.command()
    async def stats(self, ctx):
        embedToSend = discord.Embed(colour = discord.Colour.blurple())

    @commands.command()
    async def ping(self, ctx):
        
        await ctx.send(":ping_pong: | {}ms".format(round(self.client.latency * 1000)))

    @commands.command()
    async def approval(self, ctx):
        average = 0
        await ctx.send('**Our average rating is {}:star:'.format(round(average, 2)))

    @commands.command()
    async def blacklist(self, ctx, mode = None, user: discord.User = None):

        if self.blacklistLogObj is None:
            self.blacklistLogObj = None # get the blacklist log channel

        # check if the user running the command is a sommelier here

        if mode.lower() == 'add':
            # add to blacklist
            await ctx.send(':white_check_mark: **| Blacklisted ``{}``.**'.format(user))
            await self.blacklistLogObj.send(':triangular_flag_on_post: **| ``{}`` has been blacklisted by ``{}``.'.format(user, ctx.author))
        elif mode.lower() == 'remove':
            # remove from blacklist
            await ctx.send(':white_check_mark: **| Removed ``{}`` from the blacklist.'.format(user))
            await self.blacklistLogObj.send(':radio_button: **| ``{}`` was removed from the blacklist by ``{}``.'.format(user, ctx.author))
        else:
            await ctx.send(':x: **| Incorrect usage. ')


def setup(client):
    client.add_cog(Utility(client))