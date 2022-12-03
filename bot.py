# bot.py
import os
import re
from dotenv import load_dotenv  # responsible for loading the .env file

import discord
from discord.ext import commands, tasks
import random

import pymongo
from mongo_utility import *

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

    # display_name = message.author.display_name
    # name = message.author.name
    # mention = message.author.mention
    # guild = message.guild
    # status = message.author.status
    # top_role = message.author.top_role
    # voice_channel = message.author.voice.channel

    # get the user's discord id
    # user_id = message.author.id
    # await message.channel.send(f'User ID: {user_id}')
    # await message.channel.send(f'Display Name: {display_name}')
    # await message.channel.send(f'Name: {name}')
    # await message.channel.send(f'Mention: {mention}')
    # await message.channel.send(f'Guild: {guild}')
    # await message.channel.send(f'Status: {status}')
    # await message.channel.send(f'Roles: {top_role}')
    # await message.channel.send(f'Voice Channel: {voice_channel}')

    # ping a user id
    # await message.channel.send(f'<@{user_id}>')

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    await bot.process_commands(message)

# test command to respond to asterisk commands
@bot.command(name='rd', help='Rolls a 6 sided die')
async def roll(ctx):  # ctx is the context of the command
    res = str(random.choice(range(1, 7)))
    await ctx.send(res)


# command to add a movie to a user's watch list, stored in MongoDB
# *addMovie <movieTitle>
@bot.command(name='addMovie', help='Adds a movie to your watch list')
async def addMovie(ctx):  # ctx is the context of the command
    # you might be making a call to TMDB API to check if movie exists
    # if it does, you might be making a call to the MONGODB API to add the movie name to the database

    user_id = str(ctx.author.id)  # get the user's discord id

    user_discord_name = ctx.author.display_name  # get the user's discord name

    full_command = ctx.message.content  # the raw text that triggered this command
    ADD_MOVIE = re.compile(r'^\*addMovie (.*)$', re.IGNORECASE)  # regex to get the movie name
    match = re.match(ADD_MOVIE, full_command)  # match the regex to the full command
    
    # get the first group of the match
    if match is None:
        await ctx.send('Invalid movie to be added')
        return
    else:
        # send the movie name to the discord channel
        movie_name = match.group(1) # the first group of the match is the movie title

        #check if movie exists in the database
        if isInUserWatchList(user_id, movie_name):
            await ctx.send(f'{movie_name} is already in your watch list') # error message for the user
            return
        else:
            addToWatchList(user_id, movie_name)  # add the movie to the user's watch list
            success_string = f'Successfully added {movie_name} to {user_discord_name}\'s watch list'
            await ctx.send(success_string)  # send the success message to the discord channel


# command to remove a movie from a user's watch list, stored in MongoDB
@bot.command(name='removeMovie', help='Removes a movie from your watch list')
async def removeMovie(ctx):
    user_id = str(ctx.author.id)  # get the user's discord id

    user_discord_name = ctx.author.display_name  # get the user's discord name

    full_command = ctx.message.content  # the raw text that triggered this command
    ADD_MOVIE = re.compile(r'^\*removeMovie (.*)$', re.IGNORECASE)  # regex to get the movie name
    match = re.match(ADD_MOVIE, full_command)  # match the regex to the full command
    
    # get the first group of the match
    if match is None:
        await ctx.send('Invalid movie to be added')
        return
    else:
        # send the movie name to the discord channel
        movie_name = match.group(1) # the first group of the match is the movie title

        #check if movie exists in the database, and remove it if it does
        if isInUserWatchList(user_id, movie_name):
            removeFromUserWatchList(user_id, movie_name)  # remove the movie from the user's watch list
            success_string = f'Successfully removed {movie_name} from {user_discord_name}\'s watch list'
            await ctx.send(success_string)  # send the success message to the discord channel
        else:
            await ctx.send(f'{movie_name} is not in your watch list') # error message for the user


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