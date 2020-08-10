import discord
from discord.ext import commands

from utils import sommelier_data

class Owner(commands.Cog):

    def __init__(self, client):

        self.client = client

        self.allowedUsers = [416987805739122699, 368860954227900416]

        self.sommeliersRole = 740408576778043412
        self.sommeliersRoleObj = None

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, *, module = None):

        try:
            self.client.unload_extension(module)
            self.client.load_extension(module)
        except Exception as e:
            await ctx.send(":warning: | **ERROR:** Could not load cog ``{}``: ``{}``".format(module, str(e)))
        else:
            await ctx.send(":white_check_mark: **| Successfully reloaded module ``{}``.**".format(module))

    @commands.command()
    async def sommeliers(self, ctx, mode = None, user: discord.Member = None):

        if ctx.guild.id != 524024216463605770:
            return

        if self.sommeliersRoleObj is None:
            self.sommeliersRoleObj = ctx.guild.get_role(self.sommeliersRole)

        if ctx.author.id not in self.allowedUsers:
            return

        if mode.lower() == 'add':
            sommelier_data.Add(user.id)
            await ctx.send(":white_check_mark: **| Registered {} as a Tea Sommelier.**".format(user.name))
            await user.add_roles(self.sommeliersRoleObj)
        elif mode.lower() == 'remove':
            sommelier_data.Remove(user.id)
            await ctx.send(":white_check_mark: **| Unregistered {} as a Tea Sommelier.**".format(user.name))
            await user.remove_roles(self.sommeliersRoleObj)
        else:
            await ctx.send(':x: **| ``{}`` is not a valid mode.**'.format(mode or 'None'))

    @commands.command()
    @commands.is_owner()
    async def eval(self, ctx, *, expr):

        try:
            result = eval(expr)
            embedToSend = discord.Embed(colour = discord.Colour.green())
        except Exception as e:
            embedToSend = discord.Embed(colour = discord.Colour.red())
            result = str(e)

        embedToSend.add_field(name="Input:", value=":inbox_tray: ```{}```".format(expr), inline = False)
        embedToSend.add_field(name="Output:", value=":outbox_tray: ```{}```".format(result), inline = False)

        await ctx.send(embed = embedToSend)


def setup(client):
    client.add_cog(Owner(client))