import discord
from discord.ext import commands
import asyncio
import logging
import os
from os.path import exists
from DiscordUtils import *

logging.basicConfig(level=logging.INFO)

# String saved in environment to hide from public 
TOKEN = os.getenv('TOKEN')


# Bot Boots Up
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('Member of {} servers'.format(len(bot.servers)))
    print('------')
    
    
# Bot Joins Server
@bot.event
async def on_server_join(server):
    if exists('servers/'+server.id):
        print('Rejoining server: '+server.name)
    else:
        print('Joined new server: '+server.name)
        serverdata = open('servers/'+server.id, 'w')
        serverdata.write('work in progress')
        serverdata.close()
    # Set control character


# Bot receives Message
@bot.event
async def on_message(message):
    # Don't react to the bots messages
    if message.author == bot.user:
        return
    
    # In Private
    if message.server == None:
        print('Received Private Message')
        await bot.send_message(message.channel,'This bot does not currently accept private messages')
        
    
    # In Channel
    else:
        print('Recieved message in channel #'+message.channel.name+' on server '+message.server.name)
        await bot.process_commands(message)
        
    
    
# Server Tag Management

# ------------------------------------------------------------------------------
# Function: New Tag
# Description: Add a new tag to the server
# Usable by: Bot Commander
# Scope: Server

@bot.command(pass_context=True)
async def newtag(ctx, tag : str = None):
    """Creates a new tag
    
    Bot Commanders may use this command to add new tags to the server
    """
    
    # Check power
    if not is_BotCommander(ctx.message.author) and not ctx.message.author.permissions_in(ctx.message.channel).administrator:
        # TODO: write code...
        await sayblock('You must be a `@Bot Commander` to use this command')
        print('addtag: Not @Bot Commander')
        return
    
    server = ctx.message.server
    
    matchingTag = find_tag(server, tag)
    
    # New tag
    if not matchingTag:
        matchingTag = await create_tag(server, tag)
        await sayblock('Added Tag: '+matchingTag.mention) 
        print('Added Tag: @'+matchingTag.name)
    # Role/tag already
    else:
        # TODO: List all roles/tags matching the name
        tags = []
        roles = []
        
        for role in matchingTag:
            # Check if Tag or Role
            if is_tag(role):
                tags.append(role)
            else:
                roles.append(role)
        
        message = 'Name already exists as '
        
        
        
        if roles:
            message += 'role: \n'
            for roles in roles:
                message += '@' + role.name + '\n'
        if tags:
            message += 'tag: \n'
            for tag in tags:
                message += '@' + tag.name + '\n'
                
        #if roles DO NOT @mention
        await sayblock(message) 
        print('Tag already exists: @'+tag)


# ------------------------------------------------------------------------------
# Function: Delete Tag
# Description: Delete tag from server
# Usable by: Bot Commander
# Scope: Server

@bot.command(pass_context=True)
async def deltag(ctx, tag : str):
    """Deletes a tag
    
    Bot Commanders may use this command to delete tags from the server
    """
    # Check power
    if not is_BotCommander(ctx.message.author) and not ctx.message.author.permissions_in(ctx.message.channel).administrator:
        # TODO: write code...
        await sayblock('You must be a `@Bot Commander` to use this command')
        print('addtag: Not @Bot Commander')
        return
    
    server = ctx.message.server
    
    matchingTag = find_tag(server, tag)
    
    if matchingTag:
        # TODO: Throw error for duplicate matching tags
        await sayblock('@' + matchingTag[0].name + ' deleted')
        await bot.delete_role(server, matchingTag[0])
    else: 
        await sayblock('Tag does not exist')


# User Tag Management

# ------------------------------------------------------------------------------
# Function: Tag User
# Description: Add a tag to a user on the server
# Usable by: Bot Commander
# Scope: Server

@bot.command(pass_context=True)
async def tag(ctx, user : str, tag: str):
    """Tags a user
    
    Bot Commanders may use this command to add tags to other users
    """
    
    the = pull_context(ctx)
    
    
# Check Permissions
    if not is_BotCommander(the['message']) and not is_Admin(the['message']):
        await sayblock('You must be a `@Bot Commander` to use this command')
        print('addtag: Not @Bot Commander')
        return

# Check if tag exists
    targetTag = find_tag(the['server'], tag)[0]
    #TODO: Handle error
    
## If not bot commander or Admin or tag is on blacklist
    if on_blacklist(targetTag):
        await bot.say('No')
        return
### Return error


# Check if user exists
    target = the['server'].get_member_named(user)
    #TODO: Handle error


# Check if user already has tag
    if has_tag(target, tag):
        await bot.say('@' + target.name + ' already has that tag')
        return

# Else tag user
    await bot.add_roles(target, targetTag)
    await sayblock('@'+target.name+' has been added to @'+targetTag.name)
    print('@'+target.name+' has been tagged with @'+targetTag.name)


# ------------------------------------------------------------------------------
# Function: Remove tag from a User
# Description: Remove a tag from a user on the server
# Usable by: Bot Commander
# Scope: Server

@bot.command(pass_context=True)
async def untag(ctx, tag : str = None):
    """Untags a user
    
    Bot commanders may use this command to remove tags from other users
    """
# Check Permissions
## If not bot commander or Admin or tag is on blacklist
### Return error
# Check if tag exists
# Check if user has tag
# Else untag user



# ------------------------------------------------------------------------------
# Function: Tag Me
# Description: Add a tag to yourself
# Usable by: Everyone
# Scope: Server

@bot.command(pass_context=True, description='Tag yourself', category='User Tag Management')
async def tagme(ctx, tag : str):
    """Add tags to self
    
    Anyone may use this command to add tags to themselves
    """
    member = ctx.message.author
    
    # TODO: Check if already tagged
    
    targetRole = None
    
    for role in ctx.message.server.roles:
        if role.name.lower() == tag.lower() and is_tag(role):
            targetRole = role
    
    if targetRole != None and not on_blacklist(targetRole):
        await bot.add_roles(member, targetRole)
        await sayblock('You\'ve been added to @'+targetRole.name)
        print(member.name+' has been tagged with @'+targetRole.name)
    elif on_blacklist(targetRole):
        # TODO: Better response
        await sayblock('No')
    else:
        await sayblock('Tag does not exist')
    
# ------------------------------------------------------------------------------
# Function: Untag Me
# Description: Remove a tag from yourself
# Usable by: Everyone
# Scope: Server

@bot.command(pass_context=True)
async def untagme(ctx, tag : str):
    """Remove tags from self
    
    Anyone may use this command to remove tags from themselves
    """
    
# Check if user is has specified tag and tag not on blacklist
#

    
# Tag Information

# ------------------------------------------------------------------------------
# Function: List Tags
# Description: List tags on the server
# Usable by: Everyone
# Scope: Server

@bot.command(pass_context=True)
async def list(ctx):
    
    tags = []
    
    for role in ctx.message.server.roles:
        if is_tag(role) and not on_blacklist(role):
            tags.append(role)
    
    if tags:
        message = 'Tags on ' + ctx.message.server.name + ':\n'
    else: 
        message = 'There are no tags on the server yet'
    
    for tag in tags:
        
        message += '@' + tag.name + '\n'
        
    await sayblock(message)
        

bot.run(TOKEN)