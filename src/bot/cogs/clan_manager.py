"""
Cog to implement clan related commands. One sample impl is as follows, but implementer is free to choose their own variant.

import discord
from discord.ext import commands

class ClanManager(commands.Cog, name="clan"):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clan")
    async def clan(self, ctx):
        pass


def setup(bot) -> None:
    bot.add_cog(ClanManager(bot))
"""