from mongo_utility import *


# takes the discord name, discord id, and display name of a user and adds them to the database. Watch list will be empty and turns yielded will be 0 initially
# THIS FUNCTION IS USELESS FOR NOW
def add_user(discord_name, discord_id, display_name):
    client = getMongoClient()
    db = client["MovieBot"]
    users = db["Users"]
    user_info = {"discord_name": discord_name, "discord_id": discord_id, "display_name": display_name, "watch_list": [], "turns_yielded": 0}
    return


# returns information for all users in the database as a list of dictionaries (hashmaps)
def get_all_users():
    client = getMongoClient()
    db = client["MovieBot"]
    users = db["Users"]
    user_info = list(users.find({}))  # this queries the database for all users
    # print type of user info
    return user_info