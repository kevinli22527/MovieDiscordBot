# bot.py
import os
from dotenv import load_dotenv  # responsible for loading the .env file

import discord
from discord.ext import commands, tasks
import random

import pymongo

mongoclient = pymongo.MongoClient("mongodb+srv://KevinLi:Kevinpower1@ourcluster.eemanbw.mongodb.net/?retryWrites=true&w=majority")  # connects to the mongoDB database

load_dotenv()  # loads the .env file

TOKEN = os.getenv('DISCORD_TOKEN')  # Kevin's developer token gotten from the setup of the bot in the developer portal

import discord  # discord API

intents = discord.Intents.default()  # default bot stuff
intents.message_content = True  # allows bot to read and respond to messages

bot = commands.Bot(command_prefix='*', intents=intents)  # create connection to discord with the given intents

# called when the bot set up is complete
@bot.event  # this is a decorator
async def on_ready():
    print(f'We have logged in as {bot.user}')

# ALWAYS called when a message is sent in a channel the bot can see
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    await bot.process_commands(message)

# test command to respond to asterisk commands
@bot.command(name='rd', help='Rolls a 6 sided die')
async def roll(ctx):  # ctx is the context of the command
    res = str(random.choice(range(1, 7)))
    await ctx.send(res)


# command to add a movie to a user's watch list, stored in MongoDB
@bot.command(name='addMovie', help='Adds a movie to your watch list')
async def addMovie(ctx, movie_name):  # ctx is the context of the command
    # you might be making a call to TMDB API to check if movie exists
    # if it does, you might be making a call to the MONGODB API to add the movie name to the database

    # MAKE SURE THAT EVERYTHING THAT HAPPENS AFTER *addMovie IS CONSIDERED PART OF THE MOVIE NAME

    # NOTE: you can use the ctx.author.id to get the user's ID
    # NOTE: you can use the ctx.author.name to get the user's name
    # NOTE: you can use the ctx.author.mention to get the user's mention
    # NOTE: you can use the ctx.author.display_name to get the user's display name
    # NOTE: you can use the ctx.author.avatar_url to get the user's avatar url
    # NOTE: you can use the ctx.author.created_at to get the user's creation date
    # NOTE: you can use the ctx.author.discriminator to get the user's discriminator
    # NOTE: you can use the ctx.author.guild to get the user's guild
    # NOTE: you can use the ctx.author.joined_at to get the user's joined date
    # NOTE: you can use the ctx.author.raw_status to get the user's raw status
    # NOTE: you can use the ctx.author.status to get the user's status
    # NOTE: you can use the ctx.author.top_role to get the user's top role
    # NOTE: you can use the ctx.author.voice to get the user's voice
    # NOTE: you can use the ctx.author.voice_channel to get the user's voice channel
    # NOTE: you can use the ctx.author.web_status to get the user's web status
    
    pass


# command to remove a movie from a user's watch list, stored in MongoDB
@bot.command(name='rm', help='Removes a movie from your watch list')
async def removeMovie(ctx):
    pass


# command to rate a movie after watching it, thus removing it from the user's watch list. The movie will be placed in the combined watched list
@bot.command(name='rate', help='Rates a movie after watching it')
async def rateMovie(ctx):
    pass


# command to display whose turn it is to pick a movie
@bot.command(name='whoseTurn', help='Displays whose turn it is to pick a movie')
async def whoseTurn(ctx):
    pass


# command to get a random movie from the watchlist of the person whose turn it is to pick a movie
@bot.command(name='pick', help='Picks a random movie from the watchlist of the person whose turn it is to pick a movie')
async def pickMovie(ctx):
    pass


# command to display a user's watch list
@bot.command(name='list', help='Displays your watch list')
async def list(ctx):
    pass


# command to yield a user's turn to pick a movie
@bot.command(name='yield', help='Yields your turn to pick a movie')
async def yieldTurn(ctx):
    pass


# command to display a user's movie stats, such as their watch list and the number of turns they have yielded
@bot.command(name='stats', help='Displays the stats of a user')
async def stats(ctx):
    pass



bot.run(TOKEN)