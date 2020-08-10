import discord
from discord.ext import commands

from utils import blacklist_data, stats_data, sommelier_data

client = commands.Bot(command_prefix = ['tea!', 'Tea!', 'TEA!'])
client.remove_command('help')

TOKEN = ''

cogs = ['cogs.utility', 'cogs.feedback', 'cogs.fun', 'cogs.events', 'cogs.orders', 'cogs.owner']

for cog in cogs:
    try:
        client.load_extension(cog)
    except Exception as e:
        print('Could not add cog {} because {}'.format(cog, str(e)))

@client.event
async def on_ready():
    print("Bot is online.")

    activity = discord.Game(name = 'with tea | tea!help | v2.0.0')
    await client.change_presence(activity = activity, status = discord.Status.online)

    stats_data.WriteSingle('login')

@client.command()
async def help(ctx):

    embedToSend = discord.Embed(colour = discord.Colour.blurple())
    embedToSend.set_author(name="Discord Tea Help - Prefix: tea!")

    embedToSend.add_field(name="Ordering Commands", value="""
``tea!rules`` - See ordering rules.

``tea!order <order>`` - Order some tea. 
``tea!cancel <orderID>`` - Cancel a tea you've ordered with its ID.

``tea!quickorder <option>`` - Select a tea you'd like from a menu and get it delivered quickly!

``tea!myorders`` - See your current active orders.
``tea!oinfo <orderID>`` - Get the info of an order with its ID.
    """, inline = False)
    embedToSend.add_field(name="Feedback Commands", value="""
``tea!rate <rating>`` - Rate this service! Give a rating between 1 and 5.
``tea!feedback <comment>`` - Send feedback to the team!
``tea!approval`` - View the average rating for the service.
    """, inline = False)
    embedToSend.add_field(name="Other Commands", value="""
``tea!invite`` - Get a link to invite Discord Tea to your server, as well as an invite to the support server.
``tea!ping`` - See bot latency.
    """, inline = False)

    if sommelier_data.Check(ctx.author.id): # if sommelier
        embedToSend.add_field(name="Sommelier Commands", value="""
``tea!claim <orderID>`` - Accept an order using its ID to brew it.
``tea!random`` - Get assigned a random waiting order.
``tea!unclaim <orderID`` - If you have claimed an order and change your mind, unclaim it.
``tea!decline <orderID> <reason>`` - Decline an order using its ID.
``tea!deliver <orderID>`` - Deliver an order: get the invite to the server it was ordered in.

``tea!list`` - See all unclaimed orders.

``tea!blacklist <add/remove> <user>`` - Blacklist or unblacklist a user.
        """, inline = False)

    embedToSend.add_field(name = 'Links', value = 'Invite: [Invite me!](https://discord.com/oauth2/authorize?client_id=507004433226268699&permissions=388161&scope=bot)\nSupport server: [Join](https://discord.gg/mP8U9ey)', inline = False)

    await ctx.send(embed = embedToSend)

    stats_data.WriteSingle('help')

client.run(TOKEN)
