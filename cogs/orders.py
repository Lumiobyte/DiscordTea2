import discord
from discord.ext import commands

import random
import asyncio

from utils import sommelier_data, stats_data

# IMPORTANT INFORMATION!
# self.orderIDs entries look like this:
#
# [0] = orderer channel
# [1] = orderer user
# [2] = order contents
# [3] = order status
# [4] = brewer userid (none if there is no brewer right now)

class Orders(commands.Cog):

    def __init__(self, client):

        self.client = client

        self.orderIDs = {}
        
        self.orderCount = 0
        self.totalOrderCount = 0

        self.orderLog = 740422451380617317
        self.orderLogObj = None

        self.bypassUsers = [416987805739122699, 368860954227900416]

        self.greenteas = ["https://i.imgur.com/FhNORTN.jpg", "https://i.imgur.com/6fSgciV.jpg", "https://i.imgur.com/CBpDMuz.jpg", "https://i.imgur.com/hAFTCTg.jpg", "https://i.imgur.com/tCcHH0V.jpg"]
        self.blackteas = ["https://i.imgur.com/5sh7TfX.jpg", "https://i.imgur.com/ucaa8gx.jpg", "https://i.imgur.com/E60w7jA.jpg", "https://i.imgur.com/Ba15j7i.jpg", "https://i.imgur.com/r8VpEJR.jpg", "https://i.imgur.com/0C3vxVY.jpg", "https://i.imgur.com/9Aejbyb.jpg"]
        self.earlgreyteas = ["https://i.imgur.com/vUjOKo7.png", "https://i.imgur.com/KNJ0Cak.png", "https://i.imgur.com/7leQ6zZ.png", "https://i.imgur.com/MTBzD03.png"]
        self.icedteas = ["https://i.imgur.com/RwNO3CB.png", "https://i.imgur.com/mxzO4s2.png", "https://i.imgur.com/wQbBZMX.png", "https://i.imgur.com/5VlHPB1.png", "https://i.imgur.com/FI38WNu.png", "https://i.imgur.com/s6GGEMR.png"]
        self.bobateas = ["https://i.imgur.com/ywCyPDt.png", "https://i.imgur.com/9nhz0E5.png", "http://www.businessnewsasia.com/wp-content/uploads/2015/04/milk-tea.jpg"]
        self.milkteas = ["https://s23991.pcdn.co/wp-content/uploads/2015/12/spiced-sweet-milk-tea-recipe.jpg", "https://i2.wp.com/subbucooks.com/wp-content/uploads/2017/12/IMG_1212.jpg?fit=2585%2C1700&ssl=1", "https://cdn.cpnscdn.com/static.coupons.com/ext/kitchme/images/recipes/600x400/honey-milk-tea-hong-kong-style_55311.jpg"]


    @commands.command()
    async def order(self, ctx, *, order = None):

        if order is None:
            await ctx.send(':grey_question: **| What type of tea would you like, {}? To order, use ``tea!order <tea>`` and replace ``<tea>`` with your order.**'.format(ctx.author.mention))
            return

        if 'tea' not in order.lower():
            await ctx.send(':no_entry_sign: **| Your order must contain tea!**')
            return

        for item in ["coffee", "c0ffee", "coff33", "c0ff3e", "c0ffe3", "coff3e", "coffe3"]:
            if item in order.lower():
                await ctx.send(":rage: **| Your order contained COFFEE! You TRAITOR!!**")
                return

        orderCountUser = 0

        for orderid in self.orderIDs:
            if self.orderIDs[orderid][1] == ctx.author:
                orderCountUser += 1


        if orderCountUser >= 2 and ctx.author.id != 368860954227900416:
            await ctx.send(':no_entry_sign: **| You can\'t have more than 2 orders pending at once!**')
            return

        if self.orderCount >= 30 and ctx.author.id != 368860954227900416:
            await ctx.send(':no_entry_sign: **| The order limit of 30 active orders has been hit. Please wait while our staff complete some orders.**')
            return

        if len(order) > 300:
            await ctx.send(':no_entry_sign: **| Your order is over 300 characters long! Please keep it shorter.**')
            return

        self.orderIDs[self.totalOrderCount] = [ctx.channel, ctx.author, order, 'Waiting', None]
        self.totalOrderCount += 1
        self.orderCount += 1

        stats_data.WriteSingle('placed')

        message = ':white_check_mark: **| Your order of ``{}`` has been placed! One of our Tea Sommeliers will claim it and deliver it right here to your server!**'.format(order)

        if self.orderCount >= 18:
            message = message + '\n :warning: Discord Tea is dealing with a large number of orders right now. Service may be delayed.'


        try:
            await ctx.send(message)
        except:
            await ctx.send(message + '\n\n:pray: Please consider letting me send messages in the channel #{} your server, {}. Right now I do not have permissions to send messages there...'.format(ctx.channel.name, ctx.guild.name))

        if self.orderLogObj is None:
            self.orderLogObj = self.client.get_channel(self.orderLog)

        await self.orderLogObj.send(":inbox_tray: **| Received order of ``{}`` with ID ``{}``. Ordered by {} in server {}.**".format(order, self.totalOrderCount - 1, ctx.author, ctx.guild.name))

    @commands.command()
    async def quickorder(self, ctx, option=None):

        image = ''
        order = ''

        if self.orderLogObj is None:
            self.orderLogObj = self.client.get_channel(self.orderLog)

        if not option:
            embed = discord.Embed(color=discord.Colour.green())
            embed.add_field(name="Quick Order Menu", value="1 - Tea\n2 - Green Tea\n3 - Black Tea\n4 - Earl Grey Tea\n5 - Iced Tea\n6 - Milk Tea\n7 - Boba Tea", inline = False)
            embed.add_field(name = 'How to order:', value = 'To order, use ``tea!quickorder <number>`` with the number of the tea you want to order.', inline = False)

            await ctx.send(embed=embed)

            return     

        try:
            option = int(option)
        except:
            await ctx.send(":no_entry_sign: **| <option> must be a number!**")
            return

        if option > 7 or option < 1:
            await ctx.send(":warning: **| That's not a valid option! Use `tea!quickorder` to see options.")
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
            order = "Boba Tea"

        await ctx.send(":tea: **| Ordered a {} for you! It will be delivered soon!**".format(order))
        
        await asyncio.sleep(80)

        embedToSend = discord.Embed(colour = discord.Colour.green())
        embedToSend.add_field(name = 'Your tea has arrived!', value = 'Your {} has been brewed!'.format(order))
        embedToSend.set_image(url = image)

        await ctx.send(ctx.author.mention, embed = embedToSend)

        stats_data.WriteSingle('quickorders')

    @commands.command()
    async def myorders(self, ctx):
        usersIDs = []
        embedValue = ''
        orderCount = 0

        embedToSend = discord.Embed(color = discord.Color.teal())

        for orderID in self.orderIDs:
            if self.orderIDs[orderID][1] == ctx.author:
                usersIDs.append(orderID)

        if len(usersIDs) <= 0:
            embedToSend.add_field(name = "Your Active Orders (0)", value = "You have no active orders! Use tea!order to order something.")
        else:
            for orderID in usersIDs:
                orderCount += 1
                embedValue += 'Order ID `{}`: order of `{}` - Status: `{}`\n'.format(
                    orderID,
                    self.orderIDs[orderID][2],
                    self.orderIDs[orderID][3]
                )

            embedToSend.add_field(name = "Your active orders ({})".format(orderCount), value = embedValue)

            embedToSend.set_footer(text = 'Use tea!oinfo <id> to see more information on an order.')

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
            brewer = discord.utils.get(self.client.get_all_members(), id = order[4])
        
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

        await ctx.send(":white_check_mark: **| You canceled your order of ``{}`` with ID ``{}``.**".format(self.orderIDs[orderid][2], orderid))
        await self.orderLogObj.send(":x: **| {} canceled their order of ``{}`` with ID ``{}``.**".format(ctx.author, self.orderIDs[orderid][2], orderid))

        self.orderIDs.pop(orderid, None)
        self.orderCount -= 1

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
            embed.add_field(name = "All active orders ({})".format(order_count), value="No active orders!")
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

        await ctx.send(":white_check_mark: **| You've been assigned the order with ID ``{}``! Start brewing a ``{}``!**".format(assigned_order, self.orderIDs[assigned_order][2]))

        self.orderIDs[assigned_order][3] = "Brewing"
        self.orderIDs[assigned_order][4] = ctx.author.id

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
    
        if self.orderLogObj is None:
            self.orderLogObj = self.client.get_channel(self.orderLog)

        self.orderIDs[orderid][3] = "Brewing"
        self.orderIDs[orderid][4] = ctx.author.id


        await ctx.send(":white_check_mark: **| You claimed the order of ``{}``! Start brewing!**".format(self.orderIDs[orderid][2]))
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

            self.orderIDs.pop(orderid, None)
            self.orderCount -= 1

            return



        try:
            await ctx.author.send(":truck: **| Deliver the order to: {} in <{}>**".format(self.orderIDs[orderid][1], invite))
            await ctx.send(":white_check_mark: **| Sent you an invite to deliver!**")
        except:
            await ctx.send(":mailbox_with_mail: **| You need to open your DMs to recieve the invite to deliver!**")
            return

        await self.orderLogObj.send(":truck: **| Tea Sommelier {} is delivering the order with ID `{}`!**".format(ctx.author.name, orderid))

        try:
            await self.orderIDs[orderid][1].send(":truck: **| Tea Sommelier {} is delivering your order! Thanks for using our service!**".format(ctx.author))
        except:
            await self.orderIDs[orderid][0].send(":truck: **| {}, Tea Sommelier {} is delivering your order! Thanks for using our service!**".format(self.orderIDs[orderid][1].mention, ctx.author))

        
        self.orderIDs.pop(orderid, None)
        self.orderCount -= 1

        stats_data.WriteSingle('delivered')

def setup(client):
    client.add_cog(Orders(client))

