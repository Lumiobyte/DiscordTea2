import discord
from discord.ext import commands

from utils import sommelier_data, rating_data, blacklist_data, stats_data, sommelier_stats_data

class Owner(commands.Cog):

    def __init__(self, client):

        self.client = client

        self.allowedUsers = [416987805739122699, 368860954227900416]

        self.sommeliersRole = 740408576778043412
        self.sommeliersRoleObj = None

        self.newSommeliersRole = 749058359759601665
        self.newSommeliersRoleObj = None

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
    async def quota(self, ctx):

        if ctx.author.id not in self.allowedUsers:
            return

        notCompletedList = ''

        statsDB = sommelier_stats_data.GetAll()

        for user in statsDB:
            if statsDB[user]['totalDeliveredWeek'] < 3:
                notCompletedList += '- ``{}`` {}/3 teas brewed this week. {} declined this week.\n'.format(user, statsDB[user]['totalDeliveredWeek'], statsDB[user]['totalDeclinedWeek'])

        if notCompletedList == '':
            notCompletedList = 'No sommeliers did not meet the quota this week.'
        
        await ctx.send(notCompletedList)

    @commands.command()
    async def somlist(self, ctx):

        if ctx.author.id not in self.allowedUsers:
            return

        db = sommelier_stats_data.GetAll()

        sommelierList = ''

        for user in db:
            sommelierList += '- ``{}`` {} {}/3\n'.format(user, db[user]['totalDelivered'], db[user]['totalDeliveredWeek'])

        embed = discord.Embed(colour = discord.Colour.dark_grey)
        embed.add_field(name = 'All Sommeliers', value = sommelierList)

        await ctx.send(embed = embed)


    @commands.command()
    async def weeklyReset(self, ctx):

        def check(reaction, user):
            if reaction.emoji == '✅' and user.id == ctx.author.id:
                return True
            else:
                return False

        if ctx.author.id not in self.allowedUsers:
            return

        """
        messageSent = await ctx.send(':grey_question: **| Reset weekly statistics. Are you sure?**')
        await messageSent.add_reaction('✅')

        try:
            if reaction, user = await client.wait_for('reaction_add', timeout = 15.0, check = check) is False:
                await ctx.send(':no_entry_sign: **| Failed to authorize.**')
                return
        except:
            await ctx.send(':no_entry_sign: **| Failed to authorize.**')
            return
        """

        messageSent2 = await ctx.send(':arrows_counterclockwise: **| Please wait...**')

        sommelier_stats_data.ClearStats()
        rating_data.ClearRatings()

        await messageSent2.edit(content = ':white_check_mark: **| Reset weekly Sommelier statistics and ratings.**')

    @commands.command()
    async def sommeliers(self, ctx, mode = None, user: discord.Member = None):

        if ctx.guild.id != 524024216463605770:
            return

        if self.sommeliersRoleObj is None:
            self.sommeliersRoleObj = ctx.guild.get_role(self.sommeliersRole)

        if self.newSommeliersRoleObj is None:
            self.newSommeliersRoleObj = ctx.guild.get_role(self.newSommeliersRole)

        if ctx.author.id not in self.allowedUsers:
            return

        if mode.lower() == 'add':

            if type(user) is int:
                sommelier_data.Add(user)
                sommelier_stats_data.AddSommelier(user)
                await ctx.send(":white_check_mark: **| Registered ID {} as a Tea Sommelier.**".format(user))
            else:
                sommelier_data.Add(user.id)
                sommelier_stats_data.AddSommelier(user.id)
                await ctx.send(":white_check_mark: **| Registered {} as a Tea Sommelier.**".format(user.name))

            try:
                await user.add_roles(self.sommeliersRoleObj, self.newSommeliersRoleObj)
            except:
                pass
        elif mode.lower() == 'remove':

            if type(user) is int:
                sommelier_data.Remove(user)
                sommelier_stats_data.RemoveSommelier(user)
                await ctx.send(":white_check_mark: **| Unregistered ID {} as a Tea Sommelier.**".format(user))
            else:
                sommelier_data.Remove(user.id)
                sommelier_stats_data.AddSommelier(user.id)
                await ctx.send(":white_check_mark: **| Unregistered {} as a Tea Sommelier.**".format(user.name))

            try:
                await user.remove_roles(self.sommeliersRoleObj, self.newSommeliersRoleObj)
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
