import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

TOKEN = os.getenv('DISCORD_TOKEN')

if TOKEN is None:
    raise ValueError("No token found. Please set the DISCORD_TOKEN environment variable.")

# Define the intents
intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.tree.sync()  # Sync the commands with Discord

# Load the ScheduleController cog
async def main():
    await bot.load_extension('Controllers.schedule_controller')
    await bot.start(TOKEN)

# Define a simple slash command
@bot.tree.command(name="hello", description="Say hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello World!")

import asyncio
asyncio.run(main())