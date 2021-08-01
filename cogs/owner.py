import discord
from discord.ext import commands

import asyncio

from utils import sommelier_data, rating_data, blacklist_data, stats_data, sommelier_stats_data

class Owner(commands.Cog):

    def __init__(self, client):

        self.client = client

        self.allowedUsers = [416987805739122699, 368860954227900416]

        self.vetSommeliersRole = 761596659288375327
        self.vetSommeliersRoleObj = None

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
            await ctx.send(":warning: | **ERROR:** Could not load cog `{}`: `{}`".format(module, str(e)))
        else:
            await ctx.send(":white_check_mark: **| Successfully reloaded module `{}`.**".format(module))

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, *, module = None):

        try:
            self.client.load_extension(module)
        except Exception as e:
            await ctx.send(":warning: | **ERROR:** Could not load cog `{}`: `{}`".format(module, str(e)))
        else:
            await ctx.send(":white_check_mark: **| Successfully loaded module `{}`.**".format(module))

    @commands.command()
    @commands.is_owner()
    async def picksotw(self, ctx):

        if ctx.author.id not in self.allowedUsers:
            return

        message = await ctx.send('<a:loader:803401760210944071> **| Calculating...**')

        somstats = sommelier_stats_data.GetAll()

        toSort = {}
        sortedOrdersCompleted = None
        sortedRatings = None
        j = 0

        total = 0
        counter = 0

        for user in somstats:
            toSort[user] = somstats[user]['totalDeliveredWeek']  
        
        sortedOrdersCompleted = sorted(toSort.items(), key = lambda x: x[1], reverse=True)

        for user in sortedOrdersCompleted:

            for i in range(0, 5):
                total += (i + 1) * somstats[user[0]]['ratings'][i]
                counter += 1 * somstats[user[0]]['ratings'][i]

            ratingAverage = total / counter

            toSort[user[0]] = ratingAverage

            j += 1

            if j == 5: 
                break

        sortedRatings = sorted(toSort.items(), key = lambda x: x[1], reverse=True)

        member = await self.client.get_guild(524024216463605770).fetch_member(int(next(iter(sortedRatings))[0]))

        await message.edit(content = f':crown: **| The Sommelier of the Week is {member.mention}!**')
        await member.add_roles(self.client.get_guild(524024216463605770).get_role(750505426637815831), reason = 'SOTW')

    @commands.command()
    @commands.is_owner()
    async def fixer(self, ctx):

        sommelier_stats_data.FixDatabase()

        await ctx.send(':white_check_mark: **| Done**')

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

        userCount = 0
        helperCounter = 0
        helperValue = ''
        embedValueList = []
        embedList = []

        statsDB = sommelier_stats_data.GetAll()

        for user in statsDB:
            if statsDB[user]['totalDeliveredWeek'] < 5:
                userCount += 1
                helperCounter += 1
                helperValue += '<@{}>: {} completed  / {} declined\n'.format(user, statsDB[user]['totalDeliveredWeek'], statsDB[user]['totalDeclinedWeek'])
                if helperCounter >= 10:
                    embedValueList.append(helperValue)
                    helperCounter = 0
                    helperValue = ''

        if helperValue != '':
            embedValueList.append(helperValue)

        if userCount <= 0:
            embed = discord.Embed(color = discord.Color.green())
            embed.add_field(name = 'Sommelier Quota', value = 'No Sommeliers failed to meet quota this week.')
            await ctx.send(embed = embed)
            return

        for embedValue in embedValueList:
            embed = discord.Embed(color = discord.Color.red())
            embed.add_field(name = 'Sommelier Quota', value = embedValue)
            embedList.append(embed)

        for embed in embedList:
            await ctx.send(embed = embed)

    @commands.command()
    async def quotaremove(self, ctx):

        if ctx.author.id not in self.allowedUsers:
            return

        if self.newSommeliersRoleObj is None:
            self.newSommeliersRoleObj = ctx.guild.get_role(self.newSommeliersRole)

        if self.sommeliersRoleObj is None:
            self.sommeliersRoleObj = ctx.guild.get_role(self.sommeliersRole)

        if self.vetSommeliersRoleObj is None:
            self.vetSommeliersRoleObj = ctx.guild.get_role(self.vetSommeliersRole)

        userCount = 0
        failedDBDelete = 0
        failedRoleRemove = 0

        statsDB = sommelier_stats_data.GetAll()

        embed = discord.Embed(colour = discord.Colour.gold())
        embed.add_field(name = "Loading", value = "Please wait")

        message = await ctx.send(embed = embed)

        for user in statsDB:
            if statsDB[user]['totalDeliveredWeek'] < 5:
                userCount += 1

                try:
                    sommelier_data.Remove(str(user))
                    sommelier_stats_data.RemoveSommelier(str(user))
                except:
                    failedDBDelete += 1

                try:
                    member = ctx.guild.get_member(int(user))
                    await member.remove_roles(self.newSommeliersRoleObj, self.sommeliersRoleObj, self.vetSommeliersRoleObj)
                    await asyncio.sleep(1)
                    print(f"Full remove success! {userCount}")
                except:
                    failedRoleRemove += 1

    @commands.command()
    async def fixquotaremove(self, ctx):

        if ctx.author.id not in self.allowedUsers:
            return

        if self.newSommeliersRoleObj is None:
            self.newSommeliersRoleObj = ctx.guild.get_role(self.newSommeliersRole)

        if self.sommeliersRoleObj is None:
            self.sommeliersRoleObj = ctx.guild.get_role(self.sommeliersRole)

        if self.vetSommeliersRoleObj is None:
            self.vetSommeliersRoleObj = ctx.guild.get_role(self.vetSommeliersRole)

        await ctx.send("Working")

        statsDB = sommelier_stats_data.GetAll()

        for user in sommelier_data.GetAll():

            if sommelier_stats_data.CheckIfExists(str(user)) == False:
                sommelier_data.Remove(user)

                try:
                    member = ctx.guild.fetch_member(user)
                    await member.remove_roles(self.vetSommeliersRoleObj, self.sommeliersRoleObj, self.newSommeliersRoleObj)
                    await asyncio.sleep(1)
                except Exception as e:
                    await ctx.send(f"Fail: {str(e)}")

        await ctx.send("Done")


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

    @commands.command()
    async def somlist(self, ctx):

        if ctx.author.id not in self.allowedUsers:
            return

        userCount = 0
        helperCounter = 0
        helperValue = ''
        embedValueList = []
        embedList = []

        statsDB = sommelier_stats_data.GetAll()

        for user in statsDB:
            userCount += 1
            helperCounter += 1
            helperValue += '<@{}>: {} completed week  / {} completed total\n'.format(user, statsDB[user]['totalDeliveredWeek'], statsDB[user]['totalDelivered'])
            if helperCounter >= 10:
                embedValueList.append(helperValue)
                helperCounter = 0
                helperValue = ''

        if helperValue != '':
            embedValueList.append(helperValue)

        if userCount <= 0:
            embed = discord.Embed(color = discord.Color.red())
            embed.add_field(name = 'Sommelier List (0)', value = 'No Tea Sommeliers to display.')
            await ctx.send(embed = embed)
            return

        for embedValue in embedValueList:
            embed = discord.Embed(color = discord.Color.green())
            embed.add_field(name = 'Sommelier List ({})'.format(userCount), value = embedValue)
            embedList.append(embed)

        for embed in embedList:
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

        testApproverRole = ctx.guild.get_role(803407197081567262)

        if not testApproverRole in ctx.author.roles:
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
                await user.add_roles(self.newSommeliersRoleObj)
            except:
                pass
        elif mode.lower() == 'remove':

            if type(user) is int:
                sommelier_data.Remove(user)
                sommelier_stats_data.RemoveSommelier(user)
                await ctx.send(":white_check_mark: **| Unregistered ID {} as a Tea Sommelier.**".format(user))
            else:
                sommelier_data.Remove(user.id)
                sommelier_stats_data.RemoveSommelier(user.id)
                await ctx.send(":white_check_mark: **| Unregistered {} as a Tea Sommelier.**".format(user.name))

            try:
                await user.remove_roles(self.sommeliersRoleObj, self.newSommeliersRoleObj)
            except:
                pass
        else:

            await ctx.send(':x: **| `{}` is not a valid mode.**'.format(mode or 'None'))

    @commands.command()
    async def proof(self, ctx):
        await ctx.send("Lumiobyte#0867")


def setup(client):
    client.add_cog(Owner(client))
