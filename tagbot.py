import discord
from discord.ext import commands
import asyncio
import logging
import os
from os.path import exists
from DiscordUtils import *

logging.basicConfig(level=logging.INFO)

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
        # TODO: Scan server and offer to clean tags if any found
        # TODO: Check bot permissions and alert is insufficient
    else:
        print('Joined new server: '+server.name)
        serverdata = open('servers/'+server.id, 'w+')
        serverdata.write('work in progress\n')
        serverdata.close()
    # Set control character


# Bot receives Message
@bot.event
async def on_message(message):
    # Don't react to this bots messages
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
       

if __name__ == "__main__":
    print('Loading Extensions...')
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    
bot.run(TOKEN)