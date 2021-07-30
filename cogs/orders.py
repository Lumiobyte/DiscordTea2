import discord
from discord.ext import commands, tasks
import dbl

import datetime
import random
import asyncio

from utils import sommelier_data, stats_data, sommelier_stats_data, rating_data, config_loader

# IMPORTANT INFORMATION!
# self.orderIDs entries look like this:
#
# [0] = orderer channel
# [1] = orderer user
# [2] = order contents
# [3] = order status
# [4] = brewer userid (none if there is no brewer right now)
# [5] = ordered timestamp
# [6] = claimed timestamp (could be none if unclaimed)
#
# Same with self.waitingForRating 

# votes: simply check if an ID has a number bigger than 0

class Orders(commands.Cog):

    def __init__(self, client):

        self.client = client

        self.orderIDs = {}
        self.waitingForRating = {}
        
        self.orderCount = 0
        self.totalOrderCount = 0

        self.ttBotID = 507004433226268699
        self.bonusOrderCap = 2

        self.orderLog = 740422451380617317
        self.orderLogObj = None

        self.ratingsChannel = 740452811287822398
        self.ratingsChannelObj = None

        self.messagesLogChannel = 795895939256156160

        self.sommelierRolesDict = {'new': 749058359759601665, 'som': 740408576778043412, 'vet': 761596659288375327}
        self.sommelierRolesList = [749058359759601665, 740408576778043412, 761596659288375327]

        self.bypassUsers = [416987805739122699, 368860954227900416]

        self.newSommelierRole = 749058359759601665

        self.orderLock = False
        self.orderLockMessage = 'Tea Time is currently undergoing maintenance. You may order again soon.'

        self.greenteas = ["https://i.imgur.com/FhNORTN.jpg", "https://i.imgur.com/6fSgciV.jpg", "https://i.imgur.com/CBpDMuz.jpg", "https://i.imgur.com/hAFTCTg.jpg", "https://i.imgur.com/tCcHH0V.jpg"]
        self.blackteas = ["https://i.imgur.com/5sh7TfX.jpg", "https://i.imgur.com/ucaa8gx.jpg", "https://i.imgur.com/E60w7jA.jpg", "https://i.imgur.com/Ba15j7i.jpg", "https://i.imgur.com/r8VpEJR.jpg", "https://i.imgur.com/0C3vxVY.jpg", "https://i.imgur.com/9Aejbyb.jpg"]
        self.earlgreyteas = ["https://i.imgur.com/vUjOKo7.png", "https://i.imgur.com/KNJ0Cak.png", "https://i.imgur.com/7leQ6zZ.png", "https://i.imgur.com/MTBzD03.png"]
        self.icedteas = ["https://i.imgur.com/RwNO3CB.png", "https://i.imgur.com/mxzO4s2.png", "https://i.imgur.com/wQbBZMX.png", "https://i.imgur.com/5VlHPB1.png", "https://i.imgur.com/FI38WNu.png", "https://i.imgur.com/s6GGEMR.png"]
        self.bobateas = ["https://i.imgur.com/ywCyPDt.png", "https://i.imgur.com/9nhz0E5.png", "http://www.businessnewsasia.com/wp-content/uploads/2015/04/milk-tea.jpg"]
        self.milkteas = ["https://s23991.pcdn.co/wp-content/uploads/2015/12/spiced-sweet-milk-tea-recipe.jpg", "https://i2.wp.com/subbucooks.com/wp-content/uploads/2017/12/IMG_1212.jpg?fit=2585%2C1700&ssl=1", "https://cdn.cpnscdn.com/static.coupons.com/ext/kitchme/images/recipes/600x400/honey-milk-tea-hong-kong-style_55311.jpg"]
        self.waterGlasses = ['https://images.all-free-download.com/images/graphiclarge/glass_cup_and_water_vector_587233.jpg', 'https://gooloc.com/wp-content/uploads/vector/59/dvryfl0d0hw.jpg', 'https://ak.picdn.net/shutterstock/videos/1497607/thumb/1.jpg']
        self.halloweenTea = 'https://cdn.discordapp.com/attachments/764001485759315999/766922383985999872/image1.png'
        self.chaiTeas = ['https://www.thespruceeats.com/thmb/6B5wl61a5we2WetKu_8QmrgHkrs=/3000x1687/smart/filters:no_upscale()/how-to-make-masala-chai-tea-4134710-37c05169f2e3431f877ba5ecec6fd404.jpg', 'https://www.savoryspiceshop.com/content/mercury_modules/recipes/2/7/7/277/chai-tea-1330.jpg', 'https://i.pinimg.com/originals/39/04/58/390458633560d0fe70b0cf033fd2b6fc.jpg']

        self.dblClient = dbl.DBLClient(bot = self.client, token = config_loader.GrabToken('dbltoken'), autopost = False, webhook_port = 5001, webhook_auth = config_loader.GrabToken('dblvoteauth'), webhook_path = '/dblwebhook')

        self.votes = {}

        self.everyTenMin.start()


    @tasks.loop(seconds = 120)
    async def everyTenMin(self):
        
        toDelete = []

        for orderid in self.orderIDs:
            differenceOrdered = datetime.datetime.now() - self.orderIDs[orderid][5]
            differenceClaimed = None

            if self.orderIDs[orderid][4] != None and self.orderIDs[orderid][6] != None:
                differenceClaimed = datetime.datetime.now() - self.orderIDs[orderid][6]

            print(differenceClaimed)
            print(differenceOrdered)

            if self.orderIDs[orderid][4] != None and differenceClaimed != None:
                if differenceClaimed >= datetime.timedelta(minutes = 30) and self.orderIDs[orderid][3] == 'Brewing':

                    try:
                        await self.orderIDs[orderid][1].send(":hourglass: **| Your order of `{}` with ID `{}` has been automatically unclaimed because the Sommelier brewing it did not deliver for 30 minutes.**".format(self.orderIDs[orderid][2], orderid))
                    except:
                        await self.orderIDs[orderid][0].send(":hourglass: **| Your order of `{}` with ID `{}` has been automatically unclaimed because the Sommelier brewing it did not deliver for 30 minutes.**".format(self.orderIDs[orderid][2], orderid))

                    await self.orderLogObj.send(":hourglass: **| Order ID `{}` auto-unclaimed after 30 minutes of inactivity.**".format(orderid))

                    self.orderIDs[orderid][3] = 'Waiting'
                    self.orderIDs[orderid][4] = None

            # checking for autodelete
            if differenceOrdered:
                if differenceOrdered >= datetime.timedelta(hours = 24) and self.orderIDs[orderid][3] == 'Waiting':
                    
                    try:
                        await self.orderIDs[orderid][1].send(":wastebasket: **| Your order of `{}` with ID `{}` has been automatically cancelled because it was waiting for 24 hours.**".format(self.orderIDs[orderid][2], orderid))
                    except:
                        await self.orderIDs[orderid][0].send(":wastebasket: **| Your order of `{}` with ID `{}` has been automatically cancelled because it was waiting for 24 hours.**".format(self.orderIDs[orderid][2], orderid))

                    await self.orderLogObj.send(":wastebasket: **| Order ID `{}` was deleted from the order list after waiting for 24 hours.**".format(orderid))

                    toDelete.append(orderid)
                
              
        for orderid in toDelete: 
            stats_data.WriteSingle('declined')
            self.orderIDs.pop(orderid, None)
            self.orderCount -= 1

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        
        if data['bot'] != str(self.ttBotID):
            return

        try:
            self.votes[data['user']]
        except:
            self.votes[data['user']] = 0
        
        self.votes[data['user']] += 1

        if self.votes[data['user']] > 2:
            self.votes[data['user']] == 2

    @commands.command()
    async def lockorders(self, ctx, *, message = None):

        if ctx.author.id != 368860954227900416:
            return
        
        if self.orderLock == True:
            self.orderLock = False
        else:
            self.orderLock = True

        if message != None:
            self.orderLockMessage = message

        await ctx.send('Set order lock to `{}` and message to `{}`'.format(self.orderLock, self.orderLockMessage))

    @commands.command()
    async def order(self, ctx, *, order = None):

        if self.orderLock == True:
            await ctx.send(':warning: **| {}**'.format(self.orderLockMessage))
            return

        try:
            self.votes[str(ctx.author.id)]
        except:
            self.votes[str(ctx.author.id)] = 0

        if order is None:
            await ctx.send(':grey_question: **| What type of tea would you like, {}? To order, use `tea!order <tea>` and replace `<tea>` with your order.**'.format(ctx.author.mention))
            return

        if 'tea' not in order.lower():
            await ctx.send(':no_entry_sign: **| Your order must contain tea!**')
            return

        for item in ["coffee", "c0ffee", "coff33", "c0ff3e", "c0ffe3", "coff3e", "coffe3", "соffее", "соffee", "соffеe", "соffеe", "соffeе", "сoffee", "сoffee", "cоffee", "cоffее", "cоffеe", "cоffeе", "cоffeе", "coffeе", "coffее", "coffеe", "cofe", "coffe", "cofee", "coftea", "cofftea", "caftea", "cafftea", "latte", "late"]:
            if item in order.lower():
                await ctx.send(":rage: **| Your order contained COFFEE! You TRAITOR!!**")
                return

        for item in ['hitler', 'nazi', 'heroin', 'sex', 'piss', 'penis', 'dick', 'cock', 'semen', 'cocaine', 'faggot', 'fag', 'fags', 'nigger']:
            if item in order.lower():
                await ctx.send(":warning: **| This order is against the rules (see them with `tea!rules`). If you try to bypass this filter you will be blacklisted immediately.**")
                return

        orderCountUser = 0
        ratingWaitingUser = 0

        for orderid in self.orderIDs:
            if self.orderIDs[orderid][1] == ctx.author:
                orderCountUser += 1

        for orderid in self.waitingForRating:
            if self.waitingForRating[orderid][1] == ctx.author:
                ratingWaitingUser += 1

        if ratingWaitingUser >= 5 and ctx.author.id != 368860954227900416:
            await ctx.send(':no_entry_sign: **| You haven\'t rated 5 of your orders! Please rate them before you order more. Check `tea!myorders` to see which orders to rate.**')
            return

        if self.orderCount >= 40 and ctx.author.id != 368860954227900416:
            await ctx.send(':no_entry_sign: **| The order limit of 40 active orders has been hit. Please wait while our staff complete some orders.**')
            return

        if len(order) > 300:
            await ctx.send(':no_entry_sign: **| Your order is over 300 characters long! Please keep it shorter.**')
            return

        if orderCountUser >= 2:
            if self.votes[str(ctx.author.id)] <= 0:
                await ctx.send(':no_entry_sign: **| You can\'t have more than 2 orders pending at once! Vote for Tea Time using `tea!vote` to get another order slot.**')
                return
            else:
                self.votes[str(ctx.author.id)] -= 1
                await ctx.send(':white_check_mark: **| Extra order slot used! You have {} extra orders remaining.**'.format(self.votes[str(ctx.author.id)]))

        self.orderIDs[self.totalOrderCount] = [ctx.channel, ctx.author, order, 'Waiting', None, datetime.datetime.now(), None]
        self.totalOrderCount += 1
        self.orderCount += 1

        stats_data.WriteSingle('placed')

        message = ':white_check_mark: **| Your order of `{}` has been placed! One of our Tea Sommeliers will claim it and deliver it right here to your server!**'.format(order)

        if self.orderCount >= 18:
            message = message + '\n :warning: Tea Time is dealing with a large number of orders right now. Service may be delayed.'


        try:
            await ctx.send(message)
        except:
            await ctx.author.send(message + '\n\n:pray: Please consider letting me send messages in the channel #{} your server, {}. Right now I do not have permissions to send messages there...'.format(ctx.channel.name, ctx.guild.name))

        if self.orderLogObj is None:
            self.orderLogObj = self.client.get_channel(self.orderLog)

        await self.orderLogObj.send(":inbox_tray: **| Received order of `{}` with ID `{}`. Ordered by {} ({}) in server {} ({}).**".format(order, self.totalOrderCount - 1, ctx.author, ctx.author.id, ctx.guild.name, ctx.guild.id))

    @commands.command()
    async def quickorder(self, ctx, option=None):
        

        image = ''
        order = ''

        if self.orderLogObj is None:
            self.orderLogObj = self.client.get_channel(self.orderLog)

        if not option:
            embed = discord.Embed(color=discord.Colour.green())
            embed.add_field(name="Quick Order Menu", value="1 - Tea\n2 - Green Tea\n3 - Black Tea\n4 - Earl Grey Tea\n5 - Iced Tea\n6 - Milk Tea\n7 - Boba Tea\n8 - Water Glass\n**NEW** 9 - Chai Tea\n**NEW** 10 - Zoo Tea", inline = False)
            embed.add_field(name = 'How to order:', value = 'To order, use `tea!quickorder <number>` with the number of the tea you want to order.', inline = False)

            await ctx.send(embed=embed)

            return     

        try:
            option = int(option)
        except:
            await ctx.send(":no_entry_sign: **| <option> must be a number!**")
            return

        if option > 10 or option < 1:
            await ctx.send(":warning: **| That's not a valid option! Use `tea!quickorder` to see options.**")
            return

        if option == 1:
            image = random.choice(self.blackteas + self.greenteas + self.earlgreyteas + self.icedteas + self.milkteas + self.bobateas)
            order = "Tea"
        elif option == 2:
            image = random.choice(self.greenteas)
            order = "Green Tea"
        elif option == 3:
            image = random.choice(self.blackteas)
            order = "Black Tea"
        elif option == 4:
            image = random.choice(self.earlgreyteas)
            order = "Earl Grey Tea"
        elif option == 5:
            image = random.choice(self.icedteas)
            order = "Iced Tea"
        elif option == 6:
            image = random.choice(self.milkteas)
            order = "Milk Tea"
        elif option == 7:
            image = random.choice(self.bobateas)
            order = "Boba Tea (Bubble Tea)"
        elif option == 8:
            image = random.choice(self.waterGlasses)
            order = "Water Glass"
        elif option == 9:
            image = random.choice(self.chaiTeas)
            order = "Chai Tea"
        elif option == 10:
            self.zooteas = ["Ant Tea", "Badger Tea", "Bat Tea", "Beaver Tea", "Bee Tea", "Beetle Tea", "Bird Tea", "Bison Tea", "Blowfish Tea", "Bug Tea", "Butterfly Tea", "Camel Tea", "Cat Tea", "Cat Variant Tea", "chick Tea", "Chick Variant Tea", "Chipmunk Tea", "Cockroach Tea", "Cow Tea", "Crab Tea", "Cricket Tea", "Crocodile Tea", "Dodo Tea", "Dog Tea", "Dolphin Tea", "Dove Tea", "Dragon Tea", "Dromedary Camel Tea", "Duck Tea", "Elephant Tea", "Fish Tea", "Fish Variant Tea", "Flamingo Tea", "Fly Tea", "Giraffe Tea", "Goat Tea", "Hedgehog Tea", "Hippopotamus Tea", "Horse Tea", "Kangaroo Tea", "Lady Beetle Tea", "Leopard Tea", "Lizard Tea", "Llama Tea", "Lobster Tea", "Mammoth Tea", "Monkey Tea", "Mosquito Tea", "Mouse Tea", "Octopus Tea", "Orangutan Tea", "Otter Tea", "Owl Tea", "Ox Tea", "Parrot Tea", "Peacock Tea", "Penguin Tea", "Pig Tea", "Poodle Tea", "Rabbit Tea", "Ram Tea", "Rat Tea", "Rooster Tea", "Sauropod Tea", "Scorpion Tea", "Seal Tea", "Shark Tea", "Sheep Tea", "Shrimp Tea", "Skunk Tea", "Snail Tea", "Snake Tea", "Spider Tea", "Squid Tea", "Swan Tea", "Tiger Tea", "T-Rex Tea", "Turkey Tea", "Turtle Tea", "Water Buffalo Tea", "Whale Tea", "Whale Variant Tea", "Worm Tea"]

            # This decides our animal

            order = random.choice(self.zooteas)

            # This makes sure it has the right picture

            self.assignimage = {"Ant Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665031283933214/ant.png?width=818&height=614e", "Badger Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665034593239081/badger.png?width=818&height=614", "Bat Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665039848833094/bat.png?width=818&height=614", "Beaver Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665044268974110/beaver.png?width=818&height=614", "Bee Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665047050321960/bee.png?width=818&height=614", "Beetle Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665050963083285/beetle.png?width=818&height=614", "Bird Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665054637293588/bird.png?width=818&height=614", "Bison Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665057770700800/bison.png?width=818&height=614", "Blowfish Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665061206622218/blowfish.png?width=818&height=614", "Bug Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665066901438484/bug.png?width=818&height=614", "Butterfly Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665069867597865/butterfly.png?width=818&height=614", "Camel Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665072568205362/camel.png?width=818&height=614", "Cat Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665085348118538/cat.png?width=818&height=614", "Cat Variant Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665093590057020/cat2.png?width=818&height=614", "Chick Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665097353265172/chick.png?width=818&height=614", "Chick Variant Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665101220282408/chick2.png?width=818&height=614", "Chipmunk Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665105099096114/chipmunk.png?width=818&height=614", \
            "Cockroach Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665108395687956/cockroach.png?width=818&height=614", "Cow Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665111643258920/cow.png?width=818&height=614", "Crab Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665115443036180/crab.png?width=818&height=614", "Cricket Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665119171510292/cricket.png?width=818&height=614", "Crocodile Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665122337816626/crocodile.png?width=818&height=614", "Dodo Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665133314572328/dodo.png?width=818&height=614", "Dog Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665139287654400/dog.png?width=818&height=614", "Dolphin Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665142881255426/dolphin.png?width=818&height=614", "Dove Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665145746358302/dove.png?width=818&height=614", "Dragon Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665149231562752/dragon.png?width=818&height=614", "Dromedary Camel Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665152080543744/dromedarycamel.png?width=818&height=614", "Duck Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665155540189215/duck.png?width=818&height=614", "Elephant Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665158056378398/elephant.png?width=818&height=614", "Fish Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665161168814120/fish.png?width=818&height=614", "Fish Variant Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665164343509003/fish2.png?width=818&height=614", "Flamingo Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665177514016798/flamingo.png?width=818&height=614", "Fly Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665184443138128/fly.png?width=818&height=614", \
            "Giraffe Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665187467231232/giraffe.png?width=818&height=614", "Goat Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665190470352936/goat.png?width=818&height=614", "Hedgehog Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665192693202984/hedgehog.png?width=818&height=614", "Hippopotamus Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665194866638868/hippopotamus.png?width=818&height=614", "Horse Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665450730979348/horse.png?width=818&height=614", "Kangaroo Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665452966150174/kangaroolumiobyte.png?width=818&height=614", "Lady Beetle Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665456724246538/ladybeetle.png?width=818&height=614", "Leopard Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665459882950706/leopard.png?width=818&height=614", "Lizard Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665462953443328/lizard.png?width=818&height=614", "Llama Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665466224476190/llama.png?width=818&height=614", "Lobster Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665469995679774/lobster.png?width=818&height=614", "Mammoth Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665473736736788/mammoth.png?width=818&height=614", "Monkey Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665477490245633/monkey.png?width=818&height=614", "Mosquito Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665530724745256/mosquito.png?width=818&height=614", "Mouse Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665533844914216/mouse.png?width=818&height=614", \
            "Octopus Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665540589879306/octopus.png?width=818&height=614", "Orangutan Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665544423342090/orangutan.png?width=818&height=614", "Otter Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665549356105758/otter.png?width=818&height=614", "Owl Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665554083479562/owl.png?width=818&height=614", "Ox Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665556427440128/ox.png?width=818&height=614", "Parrot Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665560282529802/parrot.png?width=818&height=614", "Peacock Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665566481055744/peacock.png?width=818&height=614  ", "Penguin Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665582801354762/penguin.png?width=818&height=614  ", "Pig Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665587398705222/pig.png?width=818&height=614", "Poodle Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665590322266122/poodle.png?width=818&height=614", "Rabbit Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665593874710558/rabbit.png?width=818&height=614", "Ram Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665597007200346/ram.png?width=818&height=614", "Rat Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665600371163186/rat.png?width=818&height=614", "Rooster Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665603903553546/rooster.png?width=818&height=614", "Sauropod Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665607312605224/sauropod.png?width=818&height=614", "Scorpion Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665610336829440/scorpion.png?width=818&height=614", "Seal Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665614245789706/seal.png?width=818&height=614", "Shark Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665625444450355/shark.png?width=818&height=614", \
            "Sheep Tea" : "https://media.discordapp.net/attachments/782443386354663444/801664947892781066/sheep.png?width=756&height=567", "Shrimp Tea" : "https://media.discordapp.net/attachments/782443386354663444/801664951931371526/shrimp.png?width=756&height=567", "Skunk Tea" : "https://media.discordapp.net/attachments/782443386354663444/801664955610038312/skunk.png?width=756&height=567", "Snail Tea" : "https://media.discordapp.net/attachments/782443386354663444/801664959075057674/snail.png?width=756&height=567", "Snake Tea" : "https://media.discordapp.net/attachments/782443386354663444/801664961939243018/snake.png?width=756&height=567", "Spider Tea" : "https://media.discordapp.net/attachments/782443386354663444/801664965441486888/spider.png?width=756&height=567", "Squid Tea" : "https://media.discordapp.net/attachments/782443386354663444/801664968096219136/squid.png?width=756&height=567", "Swan Tea" : "https://media.discordapp.net/attachments/782443386354663444/801664971263574067/swan.png?width=818&height=614", "Tiger Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665716776206346/tiger.png?width=818&height=614 ", "T-Rex Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665719866753024/trex.png?width=818&height=614", "Turkey Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665724317302784/turkey.png?width=818&height=614", "Turtle Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665726401347594/turtle.png?width=818&height=614", "Water Buffalo Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665730328002560/waterbuffalo.png?width=818&height=614", "Whale Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665733230329886/whale.png?width=818&height=614", "Whale Variant Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665737327771658/whale2.png?width=818&height=614", "Worm Tea" : "https://media.discordapp.net/attachments/782443386354663444/801665740280430613/worm.png?width=818&height=614"}
            
            image = self.assignimage[order]

        await ctx.send(":tea: **| Ordered a {} for you! It will be delivered soon!**".format(order))
        
        await asyncio.sleep(80)

        embedToSend = discord.Embed(colour = discord.Colour.green())
        embedToSend.add_field(name = 'Your tea has arrived!', value = 'Your {} has been brewed!'.format(order))
        embedToSend.set_image(url = image)        

        await ctx.send(ctx.author.mention, embed = embedToSend)

        stats_data.WriteSingle('quickorders')

    @commands.command()
    async def myorders(self, ctx):

        try:
            self.votes[str(ctx.author.id)]
        except:
            self.votes[str(ctx.author.id)] = 0

        usersIDs = []
        usersWaiting = []
        embedValue = ''
        embedValueWaiting = ''
        orderCount = 0
        orderCountWaiting = 0

        embedToSend = discord.Embed(color = discord.Color.teal())

        for orderID in self.orderIDs:
            if self.orderIDs[orderID][1] == ctx.author:
                usersIDs.append(orderID)

        if len(usersIDs) <= 0:
            embedToSend.add_field(name = "Your Active Orders (0)", value = "You have no active orders! Use `tea!order` to order something. Use `tea!vote` to vote for Tea Time and get an extra order slot!", inline = False)
        else:
            for orderID in usersIDs:
                orderCount += 1
                embedValue += 'Order ID `{}`: order of `{}` - Status: `{}`\n'.format(
                    orderID,
                    self.orderIDs[orderID][2],
                    self.orderIDs[orderID][3]
                )

            embedToSend.add_field(name = "Your active orders ({})".format(orderCount), value = embedValue, inline = False)

        for orderID in self.waitingForRating:
            if self.waitingForRating[orderID][1] == ctx.author:
                usersWaiting.append(orderID)

        if len(usersWaiting) <= 0:
            embedToSend.add_field(name = "Your unrated orders (0)", value = "You have no unrated orders! Get a tea delivered and it will show up here until rated.")
        else:
            for orderID in usersWaiting:
                orderCountWaiting += 1
                embedValueWaiting += 'Order ID `{}`: order of `{}` - Status: `{}`\n'.format(
                    orderID,
                    self.waitingForRating[orderID][2],
                    'Unrated'
                )

            embedToSend.add_field(name = "Your unrated orders ({}/5)".format(orderCountWaiting), value = embedValueWaiting + '\nTo rate an order, use `tea!rate <order ID> <rating from 1 to 5>`.')
        
        embedToSend.set_footer(text = 'Use tea!oinfo <id> to see more information on an order. Use tea!vote to vote for Tea Time and get an extra order slot!')

        await ctx.send(embed = embedToSend)

    @commands.command()
    async def oinfo(self, ctx, orderid = None):

        if orderid is None:
            await ctx.send(':no_entry_sign: **| Please provide an Order ID.**')
            return

        try:
            orderid = int(orderid)
        except:
            await ctx.send(':no_entry_sign: **| An Order ID is a number!**')
            return

        try:
            self.orderIDs[orderid]
        except KeyError:
            await ctx.send(":no_entry_sign: **| No order with that ID!**")
            return

        order = self.orderIDs[orderid]

        if order[4] != None:
            brewer = self.client.get_user(self.orderIDs[orderid][4])
        
            if brewer is None:
                brewer = 'None'
        else:
            brewer = "None"
        
        embedToSend = discord.Embed(color = discord.Color.teal())

        embedToSend.add_field(name = "Order Information ({})".format(orderid), value = """**
        Customer: {} ({})
        Order ID: `{}`
        Order of: {}
        Ordered in: {}, #{}
        Order Status: {}
        Brewer: {}
        **""".format(
            order[1],
            order[1].id,
            orderid,
            order[2],
            order[0].guild, order[0],
            order[3],
            brewer
        ))

        await ctx.send(embed = embedToSend)

    @commands.command()
    async def cancel(self, ctx, orderid = None):

        if orderid is None:
            await ctx.send(':no_entry_sign: **| Please provide the Order ID of the order you want to cancel!**')
            return

        try:
            orderid = int(orderid)
        except:
            await ctx.send(':no_entry_sign: **| An Order ID is a number!**')
            return

        try:
            self.orderIDs[orderid]
        except KeyError:
            await ctx.send(":no_entry_sign: **| No order with that ID!**")
            return

        if self.orderIDs[orderid][1].id != ctx.author.id:
            await ctx.send(":lock: **| You can only cancel orders you placed!**")
            return

        if self.orderIDs[orderid][3] != 'Waiting':
            await ctx.send(':no_entry_sign: **| You can\'t cancel orders that are already being brewed!**')
            return

        if self.orderLogObj is None:
            self.orderLogObj = self.client.get_channel(self.orderLog)

        await ctx.send(":white_check_mark: **| You canceled your order of `{}` with ID `{}`.**".format(self.orderIDs[orderid][2], orderid))
        await self.orderLogObj.send(":x: **| {} canceled their order of `{}` with ID `{}`.**".format(ctx.author, self.orderIDs[orderid][2], orderid))

        stats_data.WriteSingle('declined')
        self.orderIDs.pop(orderid, None)
        self.orderCount -= 1

    @commands.command()
    @commands.is_owner()
    async def oeval(self, ctx, *, expr):

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
    @commands.cooldown(10, 2, commands.BucketType.user)
    async def message(self, ctx, orderid = None, *, message):

        # no orderid check
        if orderid is None:
            await ctx.send(':no_entry_sign: **| Please provide the Order ID of the order you want to send a message about!**')
            return

        # int check
        try:
            orderid = int(orderid)
        except:
            await ctx.send(':no_entry_sign: **| An Order ID is a number!**')
            return

        # exists check
        try:
            self.orderIDs[orderid]
        except KeyError:
            await ctx.send(":no_entry_sign: **| No order with that ID!**")
            return


        # length check
        if len(message) >= 500:
            await ctx.send(':no_entry_sign: **| That\'s a bit too long! Keep it under 500 characters.**')
            return


        # if user is som and they're brewing this order, send a message to order customer
        if sommelier_data.Check(ctx.author.id):
            if self.orderIDs[orderid][4] == ctx.author.id:

                brewer = self.client.get_user(self.orderIDs[orderid][4])

                # log
                await self.client.get_channel(self.messagesLogChannel).send(':speech_balloon: **| Message from {} ``({})`` to ``{}``: ```{}```**'.format(ctx.author, ctx.author.id, self.orderIDs[orderid][1], message))

                # msg customer
                try:
                    await self.orderIDs[orderid][1].send(':speech_balloon: **| The brewer of your order of `{}` sent you a message!**\n\n```{}```'.format(self.orderIDs[orderid][2], message))
                except:
                    await ctx.send(':mailbox_closed: **| That user has their DMs closed.**')
                else:

                    # confirmation
                    await ctx.send(':white_check_mark: **| Your message has been sent.**')

                    # stats
                    stats_data.WriteSingle('messages')

                return

        # otherwise, user is customer, and can only send if its their order and its brewing

        if self.orderIDs[orderid][1].id != ctx.author.id:
            await ctx.send(":lock: **| You can only message on behalf of orders you placed!**")
            return

        if self.orderIDs[orderid][3] != 'Brewing':
            await ctx.send(':no_entry_sign: **| That order is not currently being brewed!**')
            return

        brewer = self.client.get_user(self.orderIDs[orderid][4])

        # log
        await self.client.get_channel(self.messagesLogChannel).send(':speech_balloon: **| Message from {} ``({})`` to ``{}``: ```{}```**'.format(ctx.author, ctx.author.id, brewer, message))

        # msg brewer
        await brewer.send(':speech_balloon: **| Customer sent a message!**\n\n{}'.format(message))

        # confirmation
        await ctx.send(':white_check_mark: **| Your message has been sent.**')

        # stats
        stats_data.WriteSingle('messages')

    @commands.command(name="active-orders", aliases=["list", "list-o"])
    async def list_orders(self, ctx):

        if not ctx.guild.id == 524024216463605770:
            await ctx.send(":lock: **| This command cannot be used in this server!**")
            return

        if not sommelier_data.Check(ctx.author.id):
            await ctx.send(":lock: **| Only Tea Sommeliers can use this command!**")
            return

        order_count = 0
        helper_counter = 0
        helper_value = ''
        embed_value_list = []
        list_of_embeds = []

        for orderid in self.orderIDs:
            order_count += 1
            helper_counter += 1
            helper_value += "**ID `{}`: `{}` ordered by `{}`. Status: `{}`**\n".format(orderid, self.orderIDs[orderid][2], self.orderIDs[orderid][1], self.orderIDs[orderid][3])
            if helper_counter >= 5:
                embed_value_list.append(helper_value)
                helper_counter = 0
                helper_value = ''

        if helper_value != '':
            embed_value_list.append(helper_value)

        if order_count <= 0:
            embed = discord.Embed(color = discord.Color.red())
            embed.add_field(name = "All active orders ({})".format(order_count), value="No active orders!", inline = False)
            await ctx.send(embed = embed)
            return

        for embed_value in embed_value_list:
            embed = discord.Embed(color=discord.Color.magenta())
            embed.add_field(name = "All Active Orders ({})".format(order_count), value=embed_value)
            list_of_embeds.append(embed)

        for embed in list_of_embeds:
            embed.set_footer(text = 'Use tea!claim <id> to start brewing an order!')
            await ctx.send(embed = embed)

    @commands.command()
    async def random(self, ctx):
        unfinished_orders = []

        if not ctx.guild.id == 524024216463605770:
            await ctx.send(":lock: **| This command cannot be used in this server!**")
            return

        if not sommelier_data.Check(ctx.author.id):
            await ctx.send(":lock: **| Only Tea Sommeliers can use this command!**")
            return

        for orderid in self.orderIDs:
            if self.orderIDs[orderid][3] == "Waiting":
                unfinished_orders.append(orderid)

        if len(unfinished_orders) > 0:
            assigned_order = random.choice(unfinished_orders)
        else:
            await ctx.send(":no_entry_sign: **| There are no unclaimed orders waiting right now!**")
            return

        await ctx.send(":white_check_mark: **| You've been assigned the order with ID `{}`! Start brewing a `{}`!**".format(assigned_order, self.orderIDs[assigned_order][2]))

        self.orderIDs[assigned_order][3] = "Brewing"
        self.orderIDs[assigned_order][4] = ctx.author.id

    @commands.command()
    async def claimedorders(self, ctx, user: discord.User = None):

        if user is None:
            user = ctx.author

        if not ctx.guild.id == 524024216463605770:
            await ctx.send(":lock: **| This command cannot be used in this server!**")
            return

        if not sommelier_data.Check(ctx.author.id):
            await ctx.send(":lock: **| Only Tea Sommeliers can use this command!**")
            return

        if not sommelier_data.Check(user.id):
            await ctx.send(":lock: **| That user is not a Tea Sommelier!**")
            return

        usersIDs = []
        embedValue = ''
        orderCount = 0

        embedToSend = discord.Embed(color = discord.Color.teal())

        for orderID in self.orderIDs:
            if self.orderIDs[orderID][4] == user.id:
                usersIDs.append(orderID)

        if len(usersIDs) <= 0:
            embedToSend.add_field(name = "{}\'s Claimed Orders (0)".format(user), value = "There are no orders to show.")
        else:
            for orderID in usersIDs:
                orderCount += 1
                embedValue += 'Order ID `{}`: order of `{}` - Orderer: `{}`\n'.format(
                    orderID,
                    self.orderIDs[orderID][2],
                    self.orderIDs[orderID][1]
                )

            embedToSend.add_field(name = "{}\'s Claimed Orders ({})".format(user, orderCount), value = embedValue)

            embedToSend.set_footer(text = 'Use tea!oinfo <id> to see more information on an order.')

        await ctx.send(embed = embedToSend)
        

    @commands.command(aliases=["brew"])
    async def claim(self, ctx, orderid = None):

        if not ctx.guild.id == 524024216463605770:
            await ctx.send(":lock: **| This command cannot be used in this server!**")
            return

        if not sommelier_data.Check(ctx.author.id):
            await ctx.send(":lock: **| Only Tea Sommeliers can use this command!**")
            return

        if orderid is None:
            await ctx.send(':no_entry_sign: **| Please provide an Order ID!**')
            return

        try:
            orderid = int(orderid)
        except:
            await ctx.send(':no_entry_sign: **| An Order ID is a number!**')
            return

        try:
            self.orderIDs[orderid]
        except KeyError:
            await ctx.send(":no_entry_sign: **| No order with that ID!**")
            return

        if self.orderIDs[orderid][3] != "Waiting" and ctx.author.id not in self.bypassUsers:
            await ctx.send(":no_entry_sign: **| That order is already being processed by a sommelier!**")
            return
    
        orderCountUser = 0

        for oid in self.orderIDs:
            if self.orderIDs[oid][4] == ctx.author.id:
                orderCountUser += 1

        if orderCountUser >= 5:
            await ctx.send(':no_entry_sign: **| You can only have 5 orders claimed at once!**')
            return

        if self.orderLogObj is None:
            self.orderLogObj = self.client.get_channel(self.orderLog)

        self.orderIDs[orderid][3] = "Brewing"
        self.orderIDs[orderid][4] = ctx.author.id
        self.orderIDs[orderid][6] = datetime.datetime.now()

        await ctx.send(":white_check_mark: **| You claimed the order of `{}`! Start brewing!**".format(self.orderIDs[orderid][2]))
        await self.orderLogObj.send(":man: **| Tea sommelier {} claimed the order with ID `{}` and is now brewing it!**".format(ctx.author.name, orderid))

        try:
            await self.orderIDs[orderid][1].send(":man: **| Tea Sommelier {} claimed your order and is brewing it!**".format(ctx.author))  
        except:
            try:
                await self.orderIDs[orderid][0].send(":man: **| {}, Tea Sommelier {} claimed your order and is brewing it!**".format(self.orderIDs[orderid][1].mention, ctx.author))
            except:
                pass

    @commands.command()
    async def unclaim(self, ctx, orderid = None):

        if not ctx.guild.id == 524024216463605770:
            await ctx.send(":lock: **| This command cannot be used in this server!**")
            return

        if not sommelier_data.Check(ctx.author.id):
            await ctx.send(":lock: **| Only Tea Sommeliers can use this command!**")
            return

        if orderid is None:
            await ctx.send(':no_entry_sign: **| Please provide an Order ID!**')
            return

        try:
            orderid = int(orderid)
        except:
            await ctx.send(':no_entry_sign: **| An Order ID is a number!**')
            return

        try:
            self.orderIDs[orderid]
        except KeyError:
            await ctx.send(":no_entry_sign: **| No order with that ID!**")
            return

        if self.orderLogObj is None:
            self.orderLogObj = self.client.get_channel(self.orderLog)

        if self.orderIDs[orderid][4] != ctx.author.id:
            await ctx.send(":x: **| You haven't claimed this order! You can only unclaim order you have already claimed.**")
            return
        

        self.orderIDs[orderid][3] = "Waiting"
        self.orderIDs[orderid][4] = None
        self.orderIDs[orderid][6] = None

        await ctx.send(":white_check_mark: **| You unclaimed the order with ID `{}`.**".format(orderid))
        await self.orderLogObj.send(":x: **| Tea Sommelier {} unclaimed the order with ID `{}`.**".format(ctx.author.name, orderid))
        try:
            await self.orderIDs[orderid][1].send(":x: **| Tea Sommelier {} unclaimed your order with ID `{}`.**".format(ctx.author, orderid))
        except:
            try:
                await self.orderIDs[orderid][0].send(":x: **| {}, Tea Sommelier {} unclaimed your order with ID `{}`.**".format(self.orderIDs[orderid][1].mention, ctx.author, orderid))
            except:
                pass

    @commands.command()
    async def decline(self, ctx, orderid = None, *, reason = None):

        if not ctx.guild.id == 524024216463605770:
            await ctx.send(":lock: **| This command cannot be used in this server!**")
            return

        if not sommelier_data.Check(ctx.author.id):
            await ctx.send(":lock: **| Only Tea Sommeliers can use this command!**")
            return

        if sommelier_stats_data.GetRank(ctx.author.id) == 'new':
            await ctx.send(':no_entry_sign: **| New Sommeliers cannot decline orders.**')
            return

        if orderid is None:
            await ctx.send(':no_entry_sign: **| Please provide an Order ID!**')
            return

        try:
            orderid = int(orderid)
        except:
            await ctx.send(':no_entry_sign: **| An Order ID is a number!**')
            return

        try:
            self.orderIDs[orderid]
        except KeyError:
            await ctx.send(":no_entry_sign: **| No order with that ID!**")
            return

        if self.orderLogObj is None:
            self.orderLogObj = self.client.get_channel(self.orderLog)

        if reason != None:
            reason = 'with reason ``' + reason + '``'

        await ctx.send(":white_check_mark: **| You declined the order with ID `{}`.**".format(orderid))
        
        await self.orderLogObj.send(":triangular_flag_on_post: **| Tea sommelier {} declined the order with ID `{}` {}.**".format(ctx.author.name, orderid, reason or 'but they didn\'t specify why'))
       
        try:
            await self.orderIDs[orderid][1].send(":triangular_flag_on_post: **| Your order of `{}` was declined by Tea Sommelier {} {}.**".format(self.orderIDs[orderid][2], ctx.author, reason or 'but they didn\'t specify why'))
        except:
            try:
                await self.orderIDs[orderid][0].send(":triangular_flag_on_post: **| {}, Your order of `{}` was declined by Tea Sommelier {} {}.**".format(self.orderIDs[orderid][1].mention, self.orderIDs[orderid][1], ctx.author, reason or 'but they didn\'t specify why'))
            except:
                pass

        sommelier_stats_data.AddOrderDeclined(ctx.author.id)

        self.orderIDs.pop(orderid, None)
        self.orderCount -= 1

        stats_data.WriteSingle('declined')

    @commands.command()
    async def deliver(self, ctx, orderid = None):

        if not ctx.guild.id == 524024216463605770:
            await ctx.send(":lock: **| This command cannot be used in this server!**")
            return

        if not sommelier_data.Check(ctx.author.id):
            await ctx.send(":lock: **| Only Tea Sommeliers can use this command!**")
            return

        if orderid is None:
            await ctx.send(':no_entry_sign: **| Please provide an Order ID!**')
            return

        try:
            orderid = int(orderid)
        except:
            await ctx.send(':no_entry_sign: **| An Order ID is a number!**')
            return

        try:
            self.orderIDs[orderid]
        except KeyError:
            await ctx.send(":no_entry_sign: **| No order with that ID!**")
            return

        if self.orderLogObj is None:
            self.orderLogObj = self.client.get_channel(self.orderLog)


        if self.orderIDs[orderid][4] != ctx.author.id:
            await ctx.send(":x: **| You haven't claimed this order! The sommelier who claimed it must deliver it.**")
            return


        if self.orderIDs[orderid][3] == "Waiting":
            await ctx.send(":no_entry_sign: **| That order is not ready for delivery!**")
            return

        try:
            invite = await self.orderIDs[orderid][0].create_invite(max_uses = 1, max_age = 86400, reason = "A Tea Sommelier is delivering tea to a user in this server.")

        except Exception as e:
            await ctx.send(":x: **| There was an error creating invite: Either lack of permissions, or the bot has been kicked from the server.**")
            await ctx.send('```{}```'.format(str(e)))

            try:
                await self.orderIDs[orderid][1].send(":x: **| The bot couldn't create an invite to your server `{}` and therefore your tea cannot be delivered. Give the bot create invite permissions and order again.**".format(self.orderIDs[orderid][0].guild.name))
            except:
                try:
                    await self.orderIDs[orderid][0].send(":x: **| {}, The bot couldn't create an invite to this server and therefore your tea cannot be delivered. Give the bot create invite permissions and order again.**".format(self.orderIDs[orderid][1].mention))
                except:
                    pass

            sommelier_stats_data.AddRecentDeliver(ctx.author.id, self.orderIDs[orderid][2])

            result = sommelier_stats_data.AddOrderDelivered(ctx.author.id)

            if type(result) == list:
                if result[0] == True:
                    await ctx.author.add_roles(ctx.guild.get_role(self.sommelierRolesDict[result[1]]))

            self.orderIDs.pop(orderid, None)
            self.orderCount -= 1

            stats_data.WriteSingle('delivered')

            return


        try:
            await ctx.author.send(":truck: **| Deliver the order to: {} in <{}>**".format(self.orderIDs[orderid][1], invite))
            await ctx.send(":white_check_mark: **| Sent you an invite to deliver!**")
        except:
            await ctx.send(":mailbox_with_mail: **| You need to open your DMs to recieve the invite to deliver!**")
            return

        await self.orderLogObj.send(":truck: **| Tea Sommelier {} is delivering the order with ID `{}`!**".format(ctx.author.name, orderid))

        try:
            await self.orderIDs[orderid][1].send(":truck: **| Tea Sommelier {} is delivering your order with ID `{}`! Thanks for using our service!**".format(ctx.author, orderid))
        except:
            await self.orderIDs[orderid][0].send(":truck: **| {}, Tea Sommelier {} is delivering your order with ID `{}`! Thanks for using our service!**".format(self.orderIDs[orderid][1].mention, ctx.author, orderid))

        sommelier_stats_data.AddRecentDeliver(ctx.author.id, self.orderIDs[orderid][2])

        result = sommelier_stats_data.AddOrderDelivered(ctx.author.id)

        if type(result) == list:
            if result[0] == True:
                await ctx.author.add_roles(ctx.guild.get_role(self.sommelierRolesDict[result[1]]))

        self.waitingForRating[orderid] = self.orderIDs[orderid]

        self.orderIDs.pop(orderid, None)
        self.orderCount -= 1

        stats_data.WriteSingle('delivered')

    @commands.command()
    async def rate(self, ctx, orderid = None, rating = None):

        if orderid is None:
            await ctx.send(':x: **| Please give an OrderID to provide a rating for!**\n\nTo get the Order ID, use `tea!myorders`')
            return

        if rating is None:
            await ctx.send(':x: **| Please give a rating between 1 and 5 stars, no decimals.**\n\nTo get the Order ID, use `tea!myorders``')
            return

        try:
            orderid = int(orderid)
        except:
            await ctx.send(":no_entry_sign: **| An OrderID is a number!**\n\nPlease provide the Order ID for the tea you want to rate.**")
            return

        try:
            rating = int(rating)
        except:
            await ctx.send(":no_entry_sign: **| Your rating must be between 1 and 5 and cannot be a decimal!**")
            return

        if rating > 5 or rating < 1:
            await ctx.send(":no_entry_sign: **| Your rating must be between 1 and 5 and cannot be a decimal!**")
            return

        try:
            self.waitingForRating[orderid]
        except:
            await ctx.send(':no_entry_sign: **| That order does not exist!**')
            return

        if ctx.author.id != self.waitingForRating[orderid][1].id:
            await ctx.send(':no_entry_sign: **| You can only provide ratings for orders that were delivered to you!**')
            return

        if self.ratingsChannelObj is None:
            self.ratingsChannelObj = self.client.get_channel(self.ratingsChannel)

        rating_data.Add(rating)
        sommelier_stats_data.AddRating(self.waitingForRating[orderid][4], rating)

        await ctx.send(":star: **| You rated your `{}` {}! Thanks for your feedback! Remember you can always support us by `tea!vote` to help us grow!**".format(self.waitingForRating[orderid][2], ':star:' * rating))

        sommelier = self.client.get_user(self.waitingForRating[orderid][4])

        await self.ratingsChannelObj.send(":star: **| Tea Sommelier {} was rated by `{}`: {}**".format(sommelier, ctx.author, ':star:' * rating))

        self.waitingForRating.pop(orderid, None)

        stats_data.WriteSingle('ratings')

def setup(client):
    client.add_cog(Orders(client))


