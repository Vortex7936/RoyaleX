import os
import sys
import datetime
import platform

from dotenv import load_dotenv
from pathlib import Path

import discord
from discord.ext import commands

from database.connection import Database
from utils.context import Context
from utils.formats import human_timedelta
from utils.logging import Logger


load_dotenv()


class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(
            command_prefix=commands.when_mentioned_or(os.getenv("PREFIX", "?")),
            intents=intents,
            allowed_mentions=discord.AllowedMentions(everyone=False),
            case_insensitive=True,
            help_command=None,
            strip_after_prefix=True,
        )

        self.logger = Logger(__name__)

        self.setup_hook()
        self.setup_cogs()

    def setup_hook(self):
        # Attempt database connection and exit on error
        try:
            self.database = Database.connect()
            self.logger.info("Successfully connected to the database.")
        except Exception as e:
            self.logger.error(e)
            sys.exit(1)

    def setup_cogs(self):
        for file in Path("src/cogs").glob("*.py"):
            name = file.stem
            try:
                self.load_extension(f"cogs.{name}")
                self.logger.info(f"Loaded extension: '{name}'")
            except Exception as e:
                self.logger.error(f"Failed to load extension '{name}': {e}")

    async def on_ready(self):
        self.logger.info(f"Logged in as {self.user} (ID: {self.user.id})")
        self.logger.info(f"Pycord Version: {discord.__version__}")
        self.logger.info(f"Python Version: {platform.python_version()}")
        self.logger.info(
            f"Running on: {platform.system()} {platform.release()} ({os.name})",
        )
        self.logger.info("------------------------------")

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        await self.process_commands(message)

    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if after.content != before.content:
            await self.process_commands(after)

    async def get_application_context(self, interaction: discord.Interaction, cls=Context):
        return await super().get_application_context(interaction, cls)

    async def on_application_command_completion(self, ctx: Context):
        executed_command = ctx.command.qualified_name.split()[0]

        if ctx.guild:
            self.logger.info(
                f"Executed '{executed_command}' command in {ctx.guild.name} (ID: {ctx.guild.id}) by {ctx.author} (ID: {ctx.author.id})"
            )
        else:
            self.logger.info(f"Executed '{executed_command}' command by {ctx.author} (ID: {ctx.author.id}) in DMs")

    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandNotFound):
            return
        else:
            self.logger.exception(f"Error while executing command '{ctx.command}':")

    async def on_application_command_error(self, ctx: Context, error: discord.DiscordException):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                color=0xE02B2B,
                description=f"You're on cooldown! Try again in `{human_timedelta(datetime.timedelta(seconds=error.retry_after))}`.",
            )
            await ctx.respond(embed=embed, ephemeral=True)

        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(color=0xE02B2B, description="You are not the owner of the bot!")
            await ctx.respond(embed=embed, ephemeral=True)

            if ctx.guild:
                self.logger.warning(
                    f"{ctx.author} (ID: {ctx.author.id}) tried to execute an owner only command in the guild {ctx.guild.name} (ID: {ctx.guild.id})"
                )
            else:
                self.logger.warning(
                    f"{ctx.author} (ID: {ctx.author.id}) tried to execute an owner only command in the bot's DMs."
                )

        elif isinstance(error, commands.BotMissingPermissions):
            missing = [
                "`" + perm.replace("_", " ").replace("guild", "server").title() + "`"
                for perm in error.missing_permissions
            ]

            embed = discord.Embed(
                color=0xE02B2B,
                description=f"I am missing the permission(s) {', '.join(missing)} to fully perform this command!",
            )
            try:
                await ctx.respond(embed=embed, ephemeral=True)
            except discord.Forbidden:
                await ctx.author.send(embed=embed)

        elif isinstance(error, commands.ConversionError):
            embed = discord.Embed(color=0xE02B2B, description=str(error.original))
            await ctx.respond(embed=embed, ephemeral=True)

        elif isinstance(error, (commands.UserInputError, commands.CheckFailure)):
            embed = discord.Embed(color=0xE02B2B, description=str(error))
            await ctx.respond(embed=embed, ephemeral=True)

        else:
            self.logger.exception(f"Error while executing command '{ctx.command}':")


if __name__ == "__main__":
    bot = Bot()
    bot.run(os.environ["BOT_TOKEN"])
