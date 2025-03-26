"""
Cog to implement user related commands. One sample impl is as follows, but implementer is free to choose their own variant.

import discord
from discord.ext import commands

class UserManager(commands.Cog, name="user"):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="link")
    async def link(self, ctx):
        pass


def setup(bot) -> None:
    bot.add_cog(UserManager(bot))
"""