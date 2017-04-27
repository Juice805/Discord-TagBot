import discord
from discord.ext import commands
import asyncio
import logging
import os
from os.path import exists


# Create bot
PREFIX = '<'
description = '''A bot which allows users to assign mentionable tags to themselves without having Role permissions'''
bot = commands.Bot(command_prefix=PREFIX, description=description)

# String saved in environment to hide from public 
TOKEN = os.getenv('DISCORD_TOKEN')
startup_extensions = ["everyone", "commanders"]


class MessageContext:
    def __init__(self, ctx):
        self.message = ctx.message
        self.author = ctx.message.author
        self.server = ctx.message.server
        self.channel = ctx.message.channel

# Reference Tag Permissions
tagPermissions = discord.Permissions.none()

# Tags that can't be added to
blacklist = ['Bot Commander','Admin']

def on_blacklist(roleName):
    
    # No admin related tags
    if 'admin' in roleName.lower():
        return True
    
    for tag in blacklist:
        if tag.lower() in roleName.lower():
            return True
    return False

def create_tag(server, tag, mentionable=True):
    return bot.create_role(server=server, name=tag, permissions=tagPermissions, position=0, mentionable=mentionable)

def is_tag(role):
    return (role.permissions == tagPermissions)
        
def get_tag(server, tag):
    # assumes only a single matching tag
    for role in server.roles:
        if role.name.lower() == tag.lower() and is_tag(role):
            return role
    return None
    
def get_tags(server, tag):
    tags = []
    # assumes only a single matching tag
    for role in server.roles:
        if role.name.lower() == tag.lower() and is_tag(role):
            tags.append(role)
    return tags
    
def get_role(server, tag):
    # assumes only a single matching tag
    for role in server.roles:
        if role.name.lower() == tag.lower():
            return role
    return None

    
def is_BotCommander(ctx):
    #TODO
    ans = False
    for role in ctx.message.author.roles:
        if role.name == 'Bot Commander':
            return True
    return ctx.message.author
    
def is_Admin(ctx):
    return ctx.message.author.permissions_in(ctx.message.channel).administrator
    
def sayblock(text: str):
    return bot.say("```"+text+"```")
    
def say(text: str):
    return bot.say(text)
    
def sayerror (short: str, long: str = ''):
    return bot.say('```[ERROR] ' + short + '```\n' + long)
    
def has_tag(user, tag):
    matched = False
    for role in user.roles:
        if role.name.lower() == tag.lower():
            matched = True
    
    return matched
    
    
