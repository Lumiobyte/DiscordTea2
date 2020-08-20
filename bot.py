import discord
from discord.ext import commands

from utils import blacklist_data, stats_data, sommelier_data

client = commands.Bot(command_prefix = ['tea!', 'Tea!', 'TEA!', 't!', 'T!'])
client.remove_command('help')

TOKEN = ''

cogs = ['cogs.utility', 'cogs.feedback', 'cogs.fun', 'cogs.events', 'cogs.orders', 'cogs.owner', 'cogs.dbl']

for cog in cogs:
    try:
        client.load_extension(cog)
    except Exception as e:
        print('Could not add cog {} because {}'.format(cog, str(e)))

@client.event
async def on_ready():
    print("Bot is online.")

    activity = discord.Game(name = 'with tea | tea!help | v2.0.2')
    await client.change_presence(activity = activity, status = discord.Status.online)

    stats_data.WriteSingle('login')

@client.command()
async def help(ctx):

    embedToSend = discord.Embed(colour = discord.Colour.blurple())
    embedToSend.set_author(name="Discord Tea Help - Prefix: tea!")

    embedToSend.add_field(name="Ordering Commands", value="""
``tea!rules`` - See ordering rules.
``tea!order <order>`` - Order some tea. 
``tea!cancel <orderID>`` - Cancel a tea you've ordered.
``tea!quickorder <option>`` - Select a tea you'd like from a menu.
``tea!myorders`` - See your current active orders.
``tea!oinfo <orderID>`` - Get the info on an order.
    """, inline = False)
    embedToSend.add_field(name="Feedback Commands", value="""
``tea!rate <rating>`` - Rate this service! Give a rating between 1 and 5.
``tea!feedback <comment>`` - Send feedback to the Sommeliers.
``tea!approval`` - View the average rating for the service.
    """, inline = False)
    embedToSend.add_field(name="Other Commands", value="""
``tea!stats`` - See Discord Tea\'s statistics.
``tea!invite`` - Get a link to invite Discord Tea to your server, as well as an invite to the support server.
``tea!ping`` - See bot latency.
``tea!tea`` :tea:
    """, inline = False)

    if sommelier_data.Check(ctx.author.id): # if sommelier
        embedToSend.add_field(name="Sommelier Commands", value="""
``tea!claim <orderID>`` - Accept an order to brew it.
``tea!random`` - Get assigned a random waiting order.
``tea!unclaim <orderID`` - Unclaim an order you claimed.
``tea!decline <orderID> <reason>`` - Decline an order.
``tea!deliver <orderID>`` - Deliver an order to the server it was ordered in.
``tea!list`` - See all unclaimed orders.
``tea!blacklist <add/remove> <user>`` - Blacklist or unblacklist a user.
        """, inline = False)

    embedToSend.add_field(name = 'Links', value = 'Invite: [Invite me!](https://discord.com/oauth2/authorize?client_id=507004433226268699&permissions=388161&scope=bot)\nSupport server: [Join](https://discord.gg/mP8U9ey)\n[Vote for me on Top.gg!](https://top.gg/bot/507004433226268699/vote)', inline = False)

    embedToSend.set_footer(text = 'Discord Tea v2.0.2 by Lumiobyte#0867 - Check tea!changelog for update changelog')

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
    
    else:

        return True

client.run(TOKEN)
