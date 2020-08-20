import discord
from discord.ext import commands

from utils import sommelier_data, rating_data, blacklist_data, stats_data

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
    @commands.is_owner()
    async def load(self, ctx, *, module = None):

        try:
            self.client.load_extension(module)
        except Exception as e:
            await ctx.send(":warning: | **ERROR:** Could not load cog ``{}``: ``{}``".format(module, str(e)))
        else:
            await ctx.send(":white_check_mark: **| Successfully loaded module ``{}``.**".format(module))

    @commands.command()
    @commands.is_owner()
    async def forceinvite(self, ctx, mode = None, *, server = None):

        if server is None:
            return

        if mode == 'name':
            serverObj = discord.utils.get(self.client.guilds, name = server)

        if mode == 'id':
            serverObj = self.client.get_guild(id = int(server))

        if serverObj is None:
            await ctx.send('Server not found')
            return

        c = None

        for c in serverObj.channels:
            if serverObj.get_channel(c.id).type == 'text':
                break

        channel = serverObj.get_channel(c.id)
                
        if channel is None:
            await ctx.send('No text channels in server')
            return

        invite = await channel.create_invite(reason = 'Bot owner requested an invite to this server.')

        await ctx.author.send('https://discord.gg/' + str(invite.code))

        

    @commands.command()
    async def sommeliers(self, ctx, mode = None, user: discord.Member = None):

        if ctx.guild.id != 524024216463605770:
            return

        if self.sommeliersRoleObj is None:
            self.sommeliersRoleObj = ctx.guild.get_role(self.sommeliersRole)

        if ctx.author.id not in self.allowedUsers:
            return

        if mode.lower() == 'add':

            if type(user) is int:
                sommelier_data.Add(user)
                await ctx.send(":white_check_mark: **| Registered ID {} as a Tea Sommelier.**".format(user))
            else:
                sommelier_data.Add(user.id)
                await ctx.send(":white_check_mark: **| Registered {} as a Tea Sommelier.**".format(user.name))

            try:
                await user.add_roles(self.sommeliersRoleObj)
            except:
                pass
        elif mode.lower() == 'remove':

            if type(user) is int:
                sommelier_data.Remove(user)
                await ctx.send(":white_check_mark: **| Unregistered ID {} as a Tea Sommelier.**".format(user))
            else:
                sommelier_data.Remove(user.id)
                await ctx.send(":white_check_mark: **| Unregistered {} as a Tea Sommelier.**".format(user.name))

            try:
                await user.remove_roles(self.sommeliersRoleObj)
            except:
                pass
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