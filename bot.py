import discord
from discord.ext import commands

client = commands.Bot(command_prefix = ['tea!', 'Tea!', 'TEA!'])
client.remove_command('help')

TOKEN = ''

cogs = ['cogs.utility', 'cogs.feedback']

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

@client.command()
async def help(ctx):

    embedToSend = discord.Embed(colour = discord.Colour.blurple())
    embedToSend.set_author(name="Discord Tea Help - Prefix: tea!")

    embedToSend.add_field(name="Commands you can use:", value="""
**tea!rules** - See ordering rules.
**tea!order <order>** - Order some tea. 
**tea!cancel <orderID>** - Cancel a tea you've ordered with its ID.
**tea!quickorder <option>** - Select a tea you'd like from a menu and get it delivered quickly!
**tea!myorders** - See your current active orders.
**tea!oinfo <orderID>** - Get the info of an order with its ID.
**tea!rate <rating>** - Rate this service! Give a rating between 1 and 5.
**tea!feedback <comment>** - Send feedback to the team!
**tea!approval** - View the average rating for the service.
**tea!invite** - Get a link to invite Discord Tea to your server, as well as an invite to the support server.
**tea!ping** - See bot latency.
    """, inline = False)

    if True: # if sommelier
        embedToSend.add_field(name="Sommelier Commands", value="""
**tea!claim <orderID>** - Accept an order using its ID to brew it.
**tea!unclaim <orderID** - If you have claimed an order and change your mind, unclaim it.
**tea!decline <orderID> <reason>** - Decline an order using its ID.
**tea!deliver <orderID>** - Deliver an order: get the invite to the server it was ordered in.
**tea!list** - See all unclaimed orders.
**tea!random** - Get assigned a random waiting order.
**tea!blacklist <add/remove> <user>** - Blacklist or unblacklist a user.
        """, inline = False)

    embedToSend.add_field(name = 'Links', value = 'Invite: [Invite me!](https://discord.com/oauth2/authorize?client_id=507004433226268699&permissions=388161&scope=bot)\nSupport server: [Join](https://discord.gg/mP8U9ey)', inline = False)

    await ctx.send(embed = embedToSend)

client.run(TOKEN)
