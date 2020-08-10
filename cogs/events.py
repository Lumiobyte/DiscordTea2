import discord
from discord.ext import commands

from utils import blacklist_data

class Events(commands.Cog):

    def __init__(self, client):

        self.client = client

        self.appealsRole = 740451813865816095
        self.appealsRoleObj = None
        self.memberRole = 740423917205848114
        self.memberRoleObj = None

        self.joinsLeavesChannel = 740451274855546963
        self.joinsLeavesChannelObj = None
        self.guildJoinsLeavesChannel = 740451402580754483
        self.guildJoinsLeavesChannelObj = None
        self.appealsChannel = 740451781389189204
        self.appealsChannelObj = None


    @commands.Cog.listener()
    async def on_member_join(self, member):

        if member.guild.id != 524024216463605770:
            return

        joinMessage = ':arrow_up_small: **{} joined the server. We are now at {} members.**'.format(member.mention, member.guild.member_count)

        if self.joinsLeavesChannelObj is None:
            self.joinsLeavesChannelObj = member.guild.get_channel(self.joinsLeavesChannel)

        if blacklist_data.Check(member.id):

            if self.appealsRoleObj is None:
                self.appealsRoleObj = member.guild.get_role(self.appealsRole)

            if self.memberRoleObj is None:
                self.memberRoleObj = member.guild.get_role(self.memberRole)

            if self.appealsChannelObj is None:
                self.appealsChannelObj = member.guild.get_channel(self.appealsChannel)

            await member.add_roles(self.appealsRoleObj, reason = 'User is blacklisted.')

            try:
                await member.remove_roles(self.memberRoleObj, reason = 'User is blacklisted.')
            except:
                pass

            await self.appealsChannelObj.send('Hello {}.\n\n**You have been blacklisted from using Discord Tea by the bot staff. This means you cannot use any of the bot\'s commands or access the server.** However, you can access this channel to appeal to bot staff and tell us why you should be unbanned.\n\nThere are no guarantees appealing here will get you unbanned from the bot, and if we do not accept your appeal, you are free to leave the server.')

            joinMessage = joinMessage + ' :warning: **Member is blacklisted!**'

        await self.joinsLeavesChannelObj.send(joinMessage)

    @commands.Cog.listener()
    async def on_member_remove(self, member):

        if member.guild.id != 524024216463605770:
            return

        leaveMessage = ':arrow_down_small: **{} left the server. We are now at {} members.**'.format(member, member.guild.member_count)

        if self.joinsLeavesChannelObj is None:
            self.joinsLeavesChannelObj = member.guild.get_channel(self.joinsLeavesChannel)

        if blacklist_data.Check(member.id):

            leaveMessage = leaveMessage + ' :warning: **Member is blacklisted!**'

        await self.joinsLeavesChannelObj.send(leaveMessage)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):

        if self.guildJoinsLeavesChannelObj is None:
            self.guildJoinsLeavesChannelObj = self.client.get_channel(self.guildJoinsLeavesChannel)

        embedToSend = discord.Embed(colour = discord.Colour.green())
        embedToSend.add_field(name = 'Joined Guild', value = ':arrow_up_small: **Discord Tea joined ``{}``\nWe now have {} servers.**'.format(guild.name, len(self.client.guilds)))

        await self.guildJoinsLeavesChannelObj.send(embed = embedToSend)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):

        if self.guildJoinsLeavesChannelObj is None:
            self.guildJoinsLeavesChannelObj = self.client.get_channel(self.guildJoinsLeavesChannel)

        embedToSend = discord.Embed(colour = discord.Colour.red())
        embedToSend.add_field(name = 'Left Guild', value = ':arrow_down_small: **Discord Tea left ``{}``\nWe now have {} servers.**'.format(guild.name, len(self.client.guilds)))

        await self.guildJoinsLeavesChannelObj.send(embed = embedToSend)






def setup(client):
    client.add_cog(Events(client))


