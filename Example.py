import discord
import asyncio
import logging
import os

logging.basicConfig(level=logging.INFO)


client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    counter = 0
    if message.content.startswith('!test'):
        
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!reset'):
        tmp = await client.send_message(message.channel, 'Resetting count...')
        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

client.run('MjAzMjk1NTg2NDk2MDIwNDgw.Cmm1RA.9rFKHQWaSatML42sgnw_zWuWrYE')