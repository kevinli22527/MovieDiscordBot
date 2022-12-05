# bot.py
import os
import re
from dotenv import load_dotenv  # responsible for loading the .env file

import discord
from discord.ext import commands, tasks
import random

import pymongo

from mongo_initialization import *
from mongo_ratings import *
from mongo_users import *
from mongo_turns import *
from mongo_watch_lists import *

from movie import *

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
        await ctx.send('Invalid command format. Should be "*addMovie <movieTitle>"')
        return
    else:
        # send the movie name to the discord channel
        movie_name = match.group(1) # the first group of the match is the movie title

        # check if the movie exists in the TMDB database
        if not movieExists(movie_name):
            await ctx.send(f'"{movie_name}" is not a valid movie title')
            return

        #check if movie exists in the user's watch list
        if isInUserWatchList(user_id, movie_name):
            await ctx.send(f'{movie_name} is already in your watch list') # error message for the user
            return
        else:
            addToWatchList(user_id, movie_name)  # add the movie to the user's watch list
            success_string = f'Successfully added {movie_name} to {user_discord_name}\'s watch list'
            await ctx.send(success_string)  # send the success message to the discord channel


# command to remove a movie from a user's watch list, stored in MongoDB
# *removeMovie <movieTitle>
@bot.command(name='removeMovie', help='Removes a movie from your watch list')
async def removeMovie(ctx):
    user_id = str(ctx.author.id)  # get the user's discord id

    user_discord_name = ctx.author.display_name  # get the user's discord name

    full_command = ctx.message.content  # the raw text that triggered this command
    REMOVE_MOVIE = re.compile(r'^\*removeMovie (.*)$', re.IGNORECASE)  # regex to get the movie name
    match = re.match(REMOVE_MOVIE, full_command)  # match the regex to the full command
    
    # get the first group of the match
    if match is None:
        await ctx.send('Invalid movie to be removed')
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


# command to rate a movie after watching it. The movie must be in the collective watched list for ratings to take effect, otherwise an error message will be displayed. Ratings will implicitly be out of the 10 scale.
# *rate <movieTitle> <rating out of 10>
@bot.command(name='rate', help='Rates a movie after watching it')
async def rateMovie(ctx):
    # get user id of who is rating
    user_id = str(ctx.author.id)  # get the user's discord id
    user_discord_name = ctx.author.display_name

    full_command = ctx.message.content  # the raw text that triggered this command
    RATE_MOVIE = re.compile(r'^\*rate (.*) (\d*)$', re.IGNORECASE)  # regex to get the movie name and the rating
    match = re.match(RATE_MOVIE, full_command)  # match the regex to the full command

    if match is None:
        await ctx.send('Invalid command format. Should be "*rate <movieTitle> <rating out of 10>"')
        return
    else: # successfully matched
        movie_name = match.group(1) # the first group of the match is the movie title
        new_rating = float(match.group(2)) # the second group of the match is the rating

        if not haveWatchedBefore(movie_name):  # check if movie has been watched before
            await ctx.send(f"Y'all have not watched {movie_name} before")
            return

        if not isValidRating(new_rating):
            await ctx.send(f"Rating must be between 0 and 10")
            return

        # get user's rating for the movie if it exists already
        old_user_rating = getUserRating(user_id, movie_name)
        # set the user's rating for the movie in the database
        addUserRating(user_id, movie_name, new_rating)

        if old_user_rating is None: # user has not rated before
            await ctx.send(f"{user_discord_name} rated {movie_name} {new_rating}/10")
        else:
            await ctx.send(f"{user_discord_name} updated their rating for {movie_name} from {old_user_rating}/10 to {new_rating}/10")
        
    return


# command to display whose turn it is to pick a movie
# *whoseTurn
@bot.command(name='whoseTurn', help='Displays whose turn it is to pick a movie')
async def whoseTurn(ctx):
    whose_turn = getWhoseTurn()["discord_name"]
    await ctx.send(f'It is {whose_turn}\'s turn to pick a movie')


# command to get a random movie from the watchlist of the person whose turn it is to pick a movie
# *pick
@bot.command(name='pick', help='Picks a random movie from the watchlist of the person whose turn it is to pick a movie')
async def pickMovie(ctx):

    whose_turn = getWhoseTurn()

    turn_user_id = whose_turn["discord_id"]
    turn_user_discord_name = whose_turn["discord_name"]
    turn_user_watch_list = whose_turn["watch_list"]

    if len(turn_user_watch_list) == 0:
        await ctx.send(f'{turn_user_discord_name} has no movies in their watch list')
        return
    else:
        random_pick = random.choice(turn_user_watch_list)
        await ctx.send(f'Random next pick for {turn_user_discord_name} is {random_pick}')

# command to display a user's watch list
# *watchList
@bot.command(name='list', help='Displays your watch list')
async def list(ctx):
    user_id = str(ctx.author.id)  # get the user's discord id

    user_discord_name = ctx.author.display_name  # get the user's discord name

    full_command = ctx.message.content  # the raw text that triggered this command
    watch_list = getUserWatchList(user_id)  # get the user's watch list from the database

    # send the user's watch list to the discord channel
    
    response = f"{user_discord_name}'s watch list:\n"
    num = 1
    for movie_name in watch_list:
        response += str(num) + ") " + movie_name + "\n"
        num += 1

    if response != f"{user_discord_name}'s watch list:\n":
        await ctx.send(response)  # send the watch list to the discord channel
    else:
        # if the user's watch list is empty, send a message to the discord channel
        await ctx.send(f'{user_discord_name}\'s watch list is empty') # error message for the user



# command to yield a user's turn to pick a movie
# *yield
# Leaving the yield turn function as simply a counter for now
@bot.command(name='yield', help='Yields your turn to pick a movie')
async def yieldTurn(ctx):
    user_id = str(ctx.author.id)  # get the user's discord id

    # ensure that non-turn people can't yield the turns of others
    if getWhoseTurn()["discord_id"] == user_id:  # right person to yield the turn
        yieldYourTurn(user_id)
        await ctx.send(f'{ctx.author.display_name} has yielded their turn to pick a movie')
    else: # wrong person to yield the turn
        await ctx.send('It is not your turn to pick a movie') # error message for the user


# command to display a user's movie stats, such as their watch list and the number of turns they have yielded
@bot.command(name='stats', help='Displays the stats of a user')
async def stats(ctx):
    user_id = str(ctx.author.id)  # get the user's discord id
    user_info = get_user_info(user_id)  # user info contains a dictionary of the user's info
    comma_separated_watch_list = ", ".join(user_info["watch_list"])  # convert the user's watch list to a comma separated string
    await ctx.send(f'{ctx.author.display_name}\'s stats:\nWatch list: {comma_separated_watch_list}\nTurns Yielded: {user_info["turns_yielded"]}')

# command to move movie from watch list to watched list; this command also switches the turn to the next person
# *watched <movieTitle>
@bot.command(name='watched', help='Moves a movie from your watch list to your watched list')
async def watched(ctx):
    user_id = str(ctx.author.id)  # get the user's discord id

    if user_id != getWhoseTurn()['discord_id']:
        await ctx.send(f'It is not your turn to pick a movie, {ctx.author.display_name}')
        return

    user_discord_name = ctx.author.display_name  # get the user's discord name

    full_command = ctx.message.content  # the raw text that triggered this command
    WATCHED_MOVIE = re.compile(r'^\*watched (.*)$', re.IGNORECASE)  # regex to get the movie name

    match = re.match(WATCHED_MOVIE, full_command)  # match the regex to the full command
    
    # get the first group of the match
    if match is None:
        await ctx.send('No movie to be moved')
        return
    else:
        # send the movie name to the discord channel
        movie_name = match.group(1) # the first group of the match is the movie title

    # check if movie exists in user list, and move to watched list if it does, else add externally without consuming a turn (mutual agreement)
    if isInUserWatchList(user_id, movie_name):
        moveFromUserWatchListToWatched(user_id, movie_name)  # move the movie from the user's watch list to the watched list
        success_string = f'Successfully moved {movie_name} from {user_discord_name}\'s watch list to watched list'
        await ctx.send(success_string)  # send the success message to the discord channel
        updateWhoseTurn()  # update whose turn it is to pick a movie
        next_turn = getWhoseTurn()["display_name"]  # get the new person whose turn it is to pick a movie
        await ctx.send(f'It is now {next_turn}\'s turn to pick a movie')  # send the new person whose turn it is to pick a movie
    else:
        # Movie is on neither watch list, but is mutually agreed upon, so add it to the watched list, without consuming a turn
        addWatchedMovie(movie_name)  # add the movie to the watched list
        await ctx.send(f'{movie_name} has been added to the watched list') # the movie doesn't have to be in the watch list to be picked

# command to display the watched list
# *watchedList
@bot.command(name='watchedList', help='Displays the watched list')
async def watchedList(ctx):
    user_id = str(ctx.author.id)  # get the user's discord id

    user_discord_name = ctx.author.display_name  # get the user's discord name

    full_command = ctx.message.content  # the raw text that triggered this command
    watched_list = getWatchedMovies()  # get the watched list from the database

    response = "Movies Watched:\n"
    num = 1
    for movie_data in watched_list:
        movie_name = movie_data['nameOfMovie']
        response += str(num) + ") " + str(movie_name) + "\n"
        num += 1

    if len(watched_list) > 0:
        await ctx.send(response)  # send the watched list to the discord channel
    else:
        # if the watched list is empty, send a message to the discord channel
        await ctx.send('No movies have been watched yet! Time to pick something good!') # error message for the user



bot.run(TOKEN)