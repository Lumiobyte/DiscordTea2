import discord
from discord.ext import commands

from utils import blacklist_data, stats_data, sommelier_data, config_loader

client = commands.AutoShardedBot(command_prefix = [';', 'tea!', 'Tea!', 'TEA!', 't!', 'T!'])
client.remove_command('help')

intents = discord.Intents.all()
intents.presences = False

TOKEN = config_loader.GrabToken('token')

cogs = ['cogs.utility', 'cogs.feedback', 'cogs.fun', 'cogs.events', 'cogs.orders', 'cogs.owner', 'cogs.dbl', 'cogs.statcord']

for cog in cogs:
    try:
        client.load_extension(cog)
    except Exception as e:
        print('Could not add cog {} because {}'.format(cog, str(e)))

@client.event
async def on_ready():
    print("Bot is online.")

    activity = discord.Game(name = 'with tea | tea!help | v2.4.0')
    await client.change_presence(activity = activity, status = discord.Status.online)

    stats_data.WriteSingle('login')

@client.command()
async def help(ctx):

    embedToSend = discord.Embed(colour = discord.Colour.blurple())
    embedToSend.set_author(name="Tea Time Help - Prefix: tea!")

    embedToSend.add_field(name="Ordering Commands", value="""
``tea!rules`` - See ordering rules.
``tea!order <order>`` - Order some tea. 
``tea!cancel <orderID>`` - Cancel a tea you've ordered.
``tea!quickorder <option>`` - Select a tea you'd like from a menu.
``tea!myorders`` - See your current active orders, and orders waiting to be rated.
``tea!oinfo <orderID>`` - Get the info on an order.
``tea!message <orderID> <message>`` - Send a message to the Tea Sommelier currently brewing your order.
    """, inline = False)
    embedToSend.add_field(name="Feedback Commands", value="""
``tea!rate <orderid> <rating>`` - Rate your tea! Provide an Order ID (find it in `tea!myorders`) and rate it from 1 to 5:star:.
``tea!feedback <comment>`` - Send feedback to the Sommeliers.
``tea!approval`` - View the overall average rating for the service.
    """, inline = False)
    embedToSend.add_field(name="Other Commands", value="""
``tea!somstats [user]`` - See the statistics of a Tea Sommelier!
``tea!privacy`` - See Tea Time\'s privacy policy
``tea!stats`` - See Tea Time\'s statistics.
``tea!invite`` - Get a link to invite Tea Time to your server, as well as an invite to the support server.
``tea!vote`` - Vote for Tea Time to get an extra order slot!
``tea!ping`` - See bot latency.
``tea!tea`` :tea:
    """, inline = False)

    if sommelier_data.Check(ctx.author.id): # if sommelier
        embedToSend.add_field(name="Sommelier Commands", value="""
``tea!claimedorders [orderID]`` - See your claimed orders, or another user\'s.
``tea!claim <orderID>`` - Accept an order to brew it.
``tea!random`` - Get assigned a random waiting order.
``tea!unclaim <orderID`` - Unclaim an order you claimed.
``tea!decline <orderID> <reason>`` - Decline an order.
``tea!deliver <orderID>`` - Deliver an order to the server it was ordered in.
``tea!list`` - See all unclaimed orders.
``tea!message <orderID> <message>`` - Send a message to the customer of an order you are brewing.
``tea!blacklist <add/remove> <user>`` - Blacklist or unblacklist a user.
        """, inline = False)

    embedToSend.add_field(name = 'Links', value = 'Invite: [Invite me!](https://discord.com/oauth2/authorize?client_id=507004433226268699&permissions=388161&scope=bot)\nSupport server: [Join](https://discord.gg/mP8U9ey)\n[Vote for me on Top.gg!](https://top.gg/bot/507004433226268699/vote)', inline = False)

    embedToSend.set_footer(text = 'Tea Time v2.4.0 by Lumiobyte#0867')

    await ctx.send(embed = embedToSend)

    stats_data.WriteSingle('help')

@client.check
async def is_blacklisted(ctx):

    if blacklist_data.Check(ctx.author.id):

        embed = discord.Embed(color=discord.Color.red())
        embed.add_field(name = "You are blacklisted.", value="You have been blacklisted and cannot use this bot.\nIf you wish to appeal, please join https://discord.gg/mP8U9ey")

        await ctx.send(embed = embed)

        return False

    else:

        return True

@client.check
async def is_in_dms(ctx):

    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(':lock: **| You can\'t use commands in DMs!**')

        return False
    
    if ctx.channel.is_nsfw() is True:
        await ctx.send(':lock: **| For the safety of Sommeliers, you cannot use commands in NSFW channels.**')

        return False
    
    else:

        return True

client.run(TOKEN)
