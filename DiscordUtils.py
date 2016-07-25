import discord
from discord.ext import commands


# Create bot

PREFIX = '<'
description = '''A bot which allows users to assign mentionable tags to themselves without having Role permissions'''
bot = commands.Bot(command_prefix=PREFIX, description=description)

# Reference Tag Permissions
tagPermissions = discord.Permissions(permissions=0)

# Tags that can't be added to
blacklist = ['Bot Commander']

def on_blacklist(role):
    for tag in blacklist:
        if role.name.lower() == tag.lower():
            return True
        else:
            return False

def create_tag(server, tag):
    return bot.create_role(server=server, name=tag, permissions=tagPermissions, position=0, mentionable=True)

def is_tag(role):
    if role.permissions == tagPermissions:
        return True
    else:
        return False
        
def find_tag(server, tag):
    tags = []
    
    for role in server.roles:
        if role.name.lower() == tag.lower() and is_tag(role):
            tags.append(role)
    return tags
    
def is_BotCommander(message):
    #TODO
    return False
    
def is_Admin(message):
    return message.author.permissions_in(message.channel).administrator
    
def sayblock(text: str):
    return bot.say("```"+text+"```")
    
def pull_context(ctx):
    data = {}
    data['message'] = ctx.message
    data['author'] = ctx.message.author
    data['server'] = ctx.message.server
    data['channel'] = ctx.message.channel
    return data
    
def has_tag(user, tag):
    matched = False
    for role in user.roles:
        if role.name.lower() == tag.lower():
            matched = True
    
    return matched