import discord
from discord.ext import commands
import asyncio
import logging
import os
from os.path import exists
from DiscordUtils import *


class Everyone():
	def __init__(self, bot):
		self.bot = bot
		
	# ------------------------------------------------------------------------------
	# Function: Tag Me
	# Description: Add a tag to yourself
	# Usable by: Everyone
	# Scope: Server

	@commands.command(pass_context=True, description='Tag yourself', category='User Tag Management')
	async def tagme(self, ctx, tag : str):
		"""Add tags to self
		
		Anyone may use this command to add tags to themselves
		"""
		the = MessageContext(ctx)
		
		if on_blacklist(tag):
			await sayerror('Blacklisted','That Tag name is blacklisted, you cannot be tagged with it.')
			return
		
		matchingTag = get_tags(the.server, tag)
		if len(matchingTag) > 1:
			await sayerror('Duplicate tag @' + matchingTag[0].name + ' detected!','Please resolve the duplicate or use the `' + PREFIX + 'clean` command to resolve automatically')
			return
		elif len(matchingTag) == 0: 
			await sayerror('Tag does not exist')
			return
			
		if matchingTag[0] in the.author.roles:
			await sayerror('@' + the.author.name + ' is already tagged with @' + matchingTag[0].name)
			return
		
		await self.bot.add_roles(the.author, matchingTag[0])
		await say('@' + the.author.name + ' has been added to @'+matchingTag[0].name)
		return
		
		
	# ------------------------------------------------------------------------------
	# Function: Untag Me
	# Description: Remove a tag from yourself
	# Usable by: Everyone
	# Scope: Server

	@commands.command(pass_context=True)
	async def untagme(self, ctx, tag : str):
		"""Remove tags from self
		
		Anyone may use this command to remove tags from themselves
		"""
		the = MessageContext(ctx)
		
		if on_blacklist(tag):
			await sayerror('Blacklisted','That Tag name is blacklisted, you cannot be tagged with it.')
			return
		
		matchingTag = get_tags(the.server, tag)
		if len(matchingTag) > 1:
			await sayerror('Duplicate tag @' + matchingTag[0].name + ' detected!','Please resolve the duplicate or use the `' + PREFIX + 'clean` command to resolve automatically')
			return
		elif len(matchingTag) == 0: 
			await sayerror('Tag does not exist')
			return
			
		if matchingTag[0] not in the.author.roles:
			await sayerror('@' + the.author.name + ' is not tagged with @' + matchingTag[0].name)
			return
		
		await self.bot.remove_roles(the.author, matchingTag[0])
		await say('@' + the.author.name + ' has been removed from @'+matchingTag[0].name)
		return

		
	# Tag Information

	# ------------------------------------------------------------------------------
	# Function: List Tags
	# Description: List tags on the server
	# Usable by: Everyone
	# Scope: Server

	@commands.command(pass_context=True)
	async def list(self, ctx):
		"""List tags on the server
		
		Anyone may use this view all tags on the server
		"""
		the = MessageContext(ctx)
		
		tags = []
		
		for role in the.server.roles:
			if is_tag(role) and not on_blacklist(role.name):
				tags.append(role)
		
		if tags:
			message = 'Tags on ' + the.server.name + ':\n'
		else: 
			message = 'There are no tags on the server yet'
			return
		
		for tag in tags:
			
			message += '• @' + tag.name +'\n'
			
		await say(message)
		return
	
def setup(bot):
	bot.add_cog(Everyone(bot))