import os
import discord
from dotenv import load_dotenv

from bot.bot import RoyaleXBot

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = RoyaleXBot(intents=intents)
bot.run(os.getenv("BOT_TOKEN"))