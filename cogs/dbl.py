import discord
from discord.ext import commands, tasks

from utils import config_loader

import topgg

class TopGG(commands.Cog):

    def __init__(self, client):
        self.client = client

        self.dbl_token = config_loader.GrabToken("dbltoken")  # set this to your bot's Top.gg token
        self.client.topggpy = topgg.DBLClient(self.client, self.dbl_token, autopost=True, post_shard_count=True)


    @commands.Cog.listener()
    async def on_autopost_success(self):
        print(
            f"Posted server count ({self.client.topggpy.guild_count}), shard count ({self.client.shard_count})"
        )


def setup(client):
    client.add_cog(TopGG(client))
