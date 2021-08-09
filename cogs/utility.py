import discord
from discord.ext import commands

import random

from utils import blacklist_data, rating_data, sommelier_data, stats_data, sommelier_stats_data, booster_data

class Utility(commands.Cog):

    def __init__(self, client):

        self.client = client

        self.blacklistLog = 740422397869424672
        self.blacklistLogObj = None

        self.staffChannel = 740411953603805285

        self.blacklistImmune = [368860954227900416, 416987805739122699]

        self.sotwRoleID = 750505426637815831

        self.subie = [
            'https://cdn.discordapp.com/attachments/717992389633114194/871300029955047434/Screenshot_20210801_105504.jpg',
            'https://cdn.discordapp.com/attachments/717992389633114194/871300525239463986/B266415-2017-WRX-STI--1--1.png',
            'https://cdn.discordapp.com/attachments/717992389633114194/871300525935710320/2Q15.jpg',
            'https://cdn.discordapp.com/attachments/717992389633114194/871301485076574268/1627804832993.jpg',
            'https://cdn.discordapp.com/attachments/717992389633114194/871301486158708766/1627804817943.jpg',
            'https://cdn.discordapp.com/attachments/717992389633114194/871301486498435092/1627804812161.jpg',
            'https://cdn.discordapp.com/attachments/717992389633114194/871301487177904169/1627804803520.jpg',
            'https://cdn.discordapp.com/attachments/717992389633114194/871301487593127987/1627804798818.jpg',
            'https://cdn.discordapp.com/attachments/717992389633114194/871301488830459924/1627804778803.jpg',
            'https://cdn.discordapp.com/attachments/717992389633114194/871301624184856586/1627804739043.jpg',
            'https://cdn.discordapp.com/attachments/717992389633114194/871301624625266778/1627804716674.jpg',
            'https://cdn.discordapp.com/attachments/717992389633114194/871301626168754226/1627804681899.jpg',
            'https://cdn.discordapp.com/attachments/717992389633114194/871302094013988884/Screenshot_20210520_125144.jpg',
            'https://cdn.discordapp.com/attachments/717992389633114194/871302093640708136/1624046601201.jpg'
        ]

    @commands.command()
    async def subaru(self, ctx):

        await ctx.message.delete()

        await ctx.send(random.choice(self.subie))

    @commands.command()
    async def rules(self, ctx):

        embedToSend = discord.Embed(colour = discord.Colour.blurple())
        embedToSend.add_field(name = 'Ordering Rules', value = """**
        • No COFFEE
        • No spammy orders (For example: "tea grsogharihgasuhgosdhgosdg")
        • No NSFW Teas
        • No Offensive Teas (Hitler/Nazi, Sexism, and/or any other forms of Racism - Communism excluded)
        • No Drugs, Medications or Poisons
        • No Human or Animal Body Parts, or Bodily Fluids
        • Orders cannot contain usernames
        • Orders cannot contain text formatting or non-Latin characters, except numbers and !#$%&<>?".
        • Orders cannot contain links.
        • Please don't use curse words in your order
        • Must Include Tea
        Please respect these rules. Breaking any of them repeatedly will result in being blacklisted from the bot and/or banned from this server.**
        """)

        await ctx.send(embed = embedToSend)

    @commands.command()
    async def invite(self, ctx):

        embedToSend = discord.Embed(colour = discord.Colour.blurple())
        embedToSend.add_field(name = 'Useful Links', value = '[Invite me to your server!](https://discord.com/oauth2/authorize?client_id=507004433226268699&permissions=388161&scope=bot)\n[Join my support server](https://discord.gg/mP8U9ey)\n[Vote for me on Top.gg!](https://top.gg/bot/507004433226268699/vote)')

        await ctx.send(embed = embedToSend)

    @commands.command()
    async def vote(self, ctx):

        embedToSend = discord.Embed(colour = discord.Colour.blurple())
        embedToSend.add_field(name = 'Vote for Tea Time to help it grow!', value = '[Click here to vote for me on Top.gg!](https://top.gg/bot/507004433226268699/vote) It will help me grow and only takes 30 seconds!')

        await ctx.send(embed = embedToSend)

    @commands.command()
    async def boosters(self, ctx):

        boostersDB = booster_data.GetAll()

        message = ''
        counter = 0

        for user in boostersDB:
            counter += 1
            message += f"- <@{user}>\n"

        await ctx.send(f"**Boosters: {counter}**\n\n" + message)

    @commands.command()
    async def amiboosting(self, ctx):

        if booster_data.Check(ctx.author.id):
            await ctx.send("You're boosting :heart:")
        else:
            await ctx.send("You're not boosting")

    @commands.command()
    async def stats(self, ctx):
        embedToSend = discord.Embed(colour = discord.Colour.blurple())

        statsDB = stats_data.GetData()

        embedToSend.add_field(name = ':bar_chart: Tea Time Stats :bar_chart:', value = """:tea: **Orders** :tea:
> Orders Placed: {}
> Teas Delivered: {}
> Orders Declined/Cancelled: {}
> Quickorders Brewed: {}
:star: **Feedback** :star:
> Ratings Given: {}
> Average Rating: {}:star:
> Feedback Comments Given: {}
> Suggestions Given: {}
> Messages Sent: {}
:card_box: **Misc** :card_box:
> Facts Told: {}
> Times it's been tea time: {}
> Times help command has been used: {}
> Times bot has logged on: {}
:chart_with_upwards_trend: **Statistics** :chart_with_upwards_trend:
> Servers: {}
> Shards: {}
> Users in support server: {}
> Tea Sommeliers: {}
> Blacklisted Users: {}

:label: **Bot Version:** 2.5.2
        """.format(
            statsDB['placed'],
            statsDB['delivered'],
            statsDB['declined'],
            statsDB['quickorders'],
            statsDB['ratings'],
            round(rating_data.GetAverage(), 2),
            statsDB['feedback'],
            statsDB['suggestions'],
            statsDB['messages'],
            statsDB['facts'],
            statsDB['teatime'],
            statsDB['help'],
            statsDB['login'],
            len(self.client.guilds),
            len(self.client.shards),
            self.client.get_guild(524024216463605770).member_count,
            sommelier_data.Amount(),
            blacklist_data.Amount()
        ))

        await ctx.send(embed = embedToSend)

    @commands.command(aliases = ['somstats'])
    async def sommelierstats(self, ctx, user: discord.User = None):
        embedToSend = discord.Embed(colour = discord.Colour.blurple())

        if user is None:
            user = ctx.author

        if sommelier_data.Check(user.id) == False:
            await ctx.send(f':no_entry_sign: **| {user} is not a Tea Sommelier!**')
            return

        statsDB = sommelier_stats_data.GetSommelier(user.id)

        if statsDB is False:
            await ctx.send(f':no_entry_sign: **| {user} is not in the statistics database.**')
            return

        total = 0
        counter = 0

        rank = ''

        if statsDB['rank'] == 'new':
            rank = '<@&749058359759601665>'
        elif statsDB['rank'] == 'som':
            rank = '<@&740408576778043412>'
        elif statsDB['rank'] == 'vet':
            rank = '**<@&761596659288375327>**'
        elif statsDB['rank'] == 'mas':
            rank = "**<@&803978659353329714>**"

        for role in ctx.author.roles:
            if role.id == 750505426637815831:
                rank = "**<@&750505426637815831>**"

        for i in range(0, 5):
            total += (i + 1) * statsDB['ratings'][i]
            counter += 1 * statsDB['ratings'][i]

        ratingAverage = round((total / counter), 2)

        ratingAverage = '`' + str(ratingAverage) + '`:star:'

        embedToSend.add_field(name = f':mag: Sommelier Stats for {user}', value = """
{}

:bar_chart: **Statistics** :bar_chart:
> Orders Delivered: `{}`
> Orders Delivered This Week: `{}/5`
> Teas Declined: `{}`
> Teas Declined This Week: `{}`
> Total Ratings This Week: `{}`
> Rating: {}\n
:truck: **Recent Deliveries:** :truck:\n- `{}`\n- `{}`\n- `{}`\n
:star: **Recent Ratings:** :star:\n{}\n{}\n{}
        """.format(
            rank,
            statsDB['totalDelivered'],
            statsDB['totalDeliveredWeek'],
            statsDB['totalDeclined'],
            statsDB['totalDeclinedWeek'],
            statsDB['totalRatings'],
            ratingAverage,
            statsDB['recentDelivered'][2],
            statsDB['recentDelivered'][1],
            statsDB['recentDelivered'][0],
            ':star:' * statsDB['recentRatings'][2],
            ':star:' * statsDB['recentRatings'][1],
            ':star:' * statsDB['recentRatings'][0]
        ))

        await ctx.send(embed = embedToSend)

    @commands.command(aliases = ['lb'])
    async def leaderboard(self, ctx, *, mode = None):

        topTen = {}
        counter = 1

        if mode is None or mode.lower() == "lifetime":
            dbSorted = sorted(sommelier_stats_data.GetAll().items(), key = lambda x: x[1]['totalDelivered'], reverse=True)

            for item in dbSorted:
                if counter <= 10:
                    topTen[item[0]] = {"rank": counter, "number": item[1]['totalDelivered'], "userid": item[0], "unit": " teas"}

                counter += 1

        elif mode.lower() == "ratings" or mode.lower() == "rating":
            
            dbRaw = sommelier_stats_data.GetAll()
            ratingsCalculated = {}

            for item in dbRaw:

                total = 0
                ratingCalcHelper = 0
                ratingAverage = 0

                for i in range(0, 5):
                    total += (i + 1) * dbRaw[item]['ratings'][i]
                    ratingCalcHelper += 1 * dbRaw[item]['ratings'][i]

                ratingAverage = round((total / ratingCalcHelper), 2)

                ratingsCalculated[item] = ratingAverage

            dbSorted = sorted(ratingsCalculated.items(), key = lambda x: x[1], reverse=True)

            for item in dbSorted:
                if counter <= 10:
                    topTen[item[0]] = {"rank": counter, "number": item[1], "userid": item[0], "unit": ":star:"}

                counter += 1

        elif mode.lower() == "weekly" or mode.lower() == "week":
            dbSorted = sorted(sommelier_stats_data.GetAll().items(), key = lambda x: x[1]['totalDeliveredWeek'], reverse=True)

            for item in dbSorted:
                if counter <= 10:
                    topTen[item[0]] = {"rank": counter, "number": item[1]['totalDeliveredWeek'], "userid": item[0], "unit": " teas"}

                counter += 1

        else:
            await ctx.send(":no_entry_sign: **| Not a valid mode. Available modes are `lifetime, ratings, weekly`")
            return

        embed = discord.Embed(colour = discord.Colour.blurple())

        embedField = ""

        for user in topTen:

            userObj = self.client.get_user(int(user))

            if topTen[user]['rank'] == 1:
                embedField += f"1. :crown: **{topTen[user]['number']}{topTen[user]['unit']} - {userObj}**\n"
            else:
                embedField += f"{topTen[user]['rank']}. {topTen[user]['number']}{topTen[user]['unit']} - {userObj}\n"

        if mode is None:
            mode = "Lifetime"

        embed.add_field(name = f":scroll: Leaderboard - {mode.capitalize()}", value = embedField)
        embed.set_footer(text = "tea!lb <lifetime | weekly | ratings> to see other categories")

        await ctx.send(embed = embed)

    @commands.command()
    async def privacy(self, ctx):

        embed = discord.Embed(colour = discord.Colour.teal())

        embed.add_field(name = 'Tea Time Privacy Policy', value = """__**What data we store**__
Tea Time stores minimal data to ensure smooth operation of the bot and all its features. The data we store **permanently** is the following:
- Statistics data: Counters of things like ratings given, orders placed, etc, all of which is displayed on the `tea!stats` command, all of which is completely anonymous and not associated with you at all
- Ratings data (amount of 1-5 star ratings given and their type, anonymous and not associated with users)
- Your Discord User ID: **ONLY** if you are blacklisted, or a Tea Sommelier

The data we store **temporarily** is the following:
- Orderer User ID
- Orderer server ID
- The ID of the channel the order was placed in
- The contents of your order
- The sommelier User ID

__**How we use this data**__
We use the data we store **permanently** to:
- Provide basic usage statistics
- Enable users to be Sommeliers
- Ensure users who break the rules and are blacklisted cannot use the bot
        """)

        embed.add_field(name = 'Tea Time Privacy Policy (continued)', value = """
We use the data we store **temporarily** to:
- Process orders
        
__**Data Security**__
Data that is associated with you can only be accessed by **Bot Admins**.

__**How to request deletion of your data**__
- Please send a friend request to `Lumiobyte#0867`.
When your data is deleted you will immediately lose any Sommelier status you may have and any active orders you have will be cleared.
**Be aware this will not remove blacklist data.**

__**About Tea Delivery - IMPORTANT!!!**__ 
When using Tea Time, please be aware that **real humans** will be **given an invite to join your server**. Consider setting up a permissions system to ensure they cannot read any private chats if you wish.

__**Note**__
We reserve the right to change this at any time without notifying users.

Last updated August 20th, 2020 
        """, inline = False)

        embed2 = discord.Embed(colour = discord.Colour.teal())
        embed2.add_field(name = 'Tea Delivery', value = """
        
        """)

        await ctx.send(embed = embed)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(":ping_pong: **| {}ms**".format(round(self.client.latency * 1000)))

    @commands.command()
    async def approval(self, ctx):
        average = rating_data.GetAverage()
        await ctx.send('**Our average rating is {}:star:**'.format(round(average, 2)))

    @commands.command()
    async def blacklist(self, ctx, mode = None, user: discord.User = None):

        if self.blacklistLogObj is None:
            self.blacklistLogObj = ctx.guild.get_channel(self.blacklistLog)

        if mode is None:
            await ctx.send(':x: **| Incorrect usage.\nExamples:\n`tea!blacklist add @Lumiobyte`\n`tea!blacklist remove 368860954227900416``**')
            return

        if user is None:
            await ctx.send(':x: **| Please provide a user to blacklist.\nExamples:\n`tea!blacklist add @Lumiobyte`\n`tea!blacklist remove 368860954227900416`**')
            return

        if not sommelier_data.Check(ctx.author.id):
            await ctx.send(':lock: **| Only Tea Sommeliers can use this command!**')
            return
                
        if user.id in self.blacklistImmune:
            await ctx.send(':no_entry_sign: **| That user is immune to being blacklisted.**')
            return
        
        if sommelier_data.Check(user.id):
            await ctx.send(':no_entry_sign: **| You can\'t blacklist a Tea Sommelier!**')
            return

        if mode.lower() == 'add':
            blacklist_data.Add(user.id)

            await ctx.send(':white_check_mark: **| Blacklisted `{}`.**'.format(user))
            await self.blacklistLogObj.send(':triangular_flag_on_post: **| `{}` has been blacklisted by `{}`.**'.format(user, ctx.author))

        elif mode.lower() == 'remove':
            result = blacklist_data.Remove(user.id)

            if result == False:
                await ctx.send(':x: **| That user is not currently blacklisted.**')
                return

            await ctx.send(':white_check_mark: **| Removed `{}` from the blacklist.**'.format(user))
            await self.blacklistLogObj.send(':radio_button: **| `{}` was removed from the blacklist by `{}`.**'.format(user, ctx.author))

        else:
            await ctx.send(':x: **| Incorrect usage.\nExamples:\n`tea!blacklist add @Lumiobyte`\n`tea!blacklist remove 368860954227900416`**')


def setup(client):
    client.add_cog(Utility(client))
