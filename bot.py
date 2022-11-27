# bot.py
import os
from dotenv import load_dotenv  # responsible for loading the .env file

import discord
from discord.ext import commands, tasks
import random

load_dotenv()  # loads the .env file

TOKEN = os.getenv('DISCORD_TOKEN')  # Kevin's developer token gotten from the setup of the bot in the developer portal

import discord

intents = discord.Intents.default()  # default bot stuff
intents.message_content = True  # allows bot to read and respond to messages

bot = commands.Bot(command_prefix='*', intents=intents)  # create connection to discord with the given intents

# called when the bot set up is complete
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# called when a message is sent in a channel the bot can see
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    await bot.process_commands(message)

@bot.command(name='rd', help='Rolls a 6 sided die')
async def roll(ctx):
    res = str(random.choice(range(1, 7)))
    await ctx.send(res)

bot.run(TOKEN)