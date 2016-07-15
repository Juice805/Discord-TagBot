import discord
import asyncio
import logging
import os
from os.path import exists

logging.basicConfig(level=logging.INFO)

# String saved in environment to hide from public 
TOKEN = os.getenv('TOKEN')

client = discord.Client()

# Bot Boots Up
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('Member of {} servers'.format(len(client.servers)))
    print('------')
    
    
# Bot Joins Server
@client.event
async def on_server_join(server):
    if exists('servers/'+server.id):
        print('Rejoining server: '+server.name)
    else:
        print('Joined new server: '+server.name)
        serverdata = open('servers/'+server.id, 'w')
        serverdata.write('work in progress')
        serverdata.close()


# Bot receives Message
@client.event
async def on_message(message):
    
    # In Private
    if message.server == None:
        print('Received Private Message')
        
    
    # In Channel
    else:
        print('Recieved Message in channel #'+message.channel.name+' on server '+message.server.name)
    

client.run(TOKEN)