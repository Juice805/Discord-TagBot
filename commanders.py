import discord
from discord.ext import commands
import asyncio
import logging
import os
from os.path import exists
from DiscordUtils import *



class Commanders():
	def __init__(self, bot):
		self.bot = bot
	# ------------------------------------------------------------------------------
	# Function: New Tag
	# Description: Add a new tag to the server
	# Usable by: Bot Commander
	# Scope: Server

	@commands.command(pass_context=True)
	async def newtag(self, ctx, tag : str, private: bool = False):
		"""Creates a new tag
		
		Bot Commanders may use this command to add new tags to the server
		"""
		the = MessageContext(ctx)
		
		# TODO: Check file for new tag's color, saved per server in JSON
		
		# Check Permissions
		if not is_BotCommander(ctx) and not is_Admin(ctx):
			await sayerror('Insufficient Permissions', 'You must be a `@Bot Commander` to use this command')
			print('addtag: Not @Bot Commander')
			return
			
		if on_blacklist(tag):
			await sayerror('Blacklisted','That Tag name is blacklisted, please choose another.')
			return
		
		if tag[0] == '@':
			tag = tag[1:]
			
		matchingTag = get_role(the.server, tag)
		
		# New tag
		if not matchingTag:
			matchingTag = await create_tag(the.server, tag, not private)
			if not private: # Add tag to bot
				memberbot = discord.utils.get(the.server.members, id=self.bot.user.id)
				await self.bot.add_roles(memberbot, matchingTag)
			await say('Tag Created: '+matchingTag.mention) 
			print('Added Tag: @'+matchingTag.name)
			return
		# Role/tag already
		else:

			message = 'Name already exists as a '
			
			if is_tag(matchingTag):
				matchedType = 'Tag'
			else:
				matchedType = 'Role'
			
			message += matchedType + '.'

			await sayerror(message) 
			print(matchedType + ' already exists: @' + matchingTag.name)
			return


	# ------------------------------------------------------------------------------
	# Function: Delete Tag
	# Description: Delete tag from server
	# Usable by: Bot Commander
	# Scope: Server

	@commands.command(pass_context=True)
	async def deltag(self, ctx, tag):
		"""Deletes a tag
		
		Bot Commanders may use this command to delete tags from the server
		"""		
		the = MessageContext(ctx)
		# Check power
		if not is_BotCommander(ctx) and not is_Admin(ctx):
			await sayerror('Insufficient Permissions', 'You must be a `@Bot Commander` to use this command')
			print('deltag: Not @Bot Commander')
			return
		
		matchingTag = get_tags(the.server, tag)
				
		if len(matchingTag) == 1:
			await self.bot.delete_role(the.server, matchingTag[0])
			await say('@' + matchingTag[0].name + ' deleted')
		elif len(matchingTag) > 1:
			await sayerror('Duplicate tag @' + matchingTag[0].name + ' detected!','Please resolve the duplicate in server settings or use the `' + PREFIX + 'clean` command to resolve automatically')
		else: 
			await sayerror('Tag does not exist')
		return


	# User Tag Management

	# ------------------------------------------------------------------------------
	# Function: Tag User
	# Description: Add a tag to a user on the server
	# Usable by: Bot Commander
	# Scope: Server

	@commands.command(pass_context=True)
	async def tag(self, ctx, tag : str, *mentions: discord.Member):
		"""Tags a user
		
		Bot Commanders may use this command to add tags to other users
		"""
		the = MessageContext(ctx)
		
		# Check power
		if not is_BotCommander(ctx) and not is_Admin(ctx):
			await sayerror('Insufficient Permissions', 'You must be a `@Bot Commander` to use this command')
			print('tag: Not @Bot Commander')
			return
					
		matchingTag = get_tags(the.server, tag)
		if len(matchingTag) > 1:
			await sayerror('Duplicate tag @' + matchingTag[0].name + ' detected!','Please resolve the duplicate in server settings or use the `' + PREFIX + 'clean` command to resolve automatically')
			return
		elif len(matchingTag) == 0: 
			await sayerror('Tag does not exist')
			return
		
		addedusers = ''
		for member in mentions:
			if self.bot.user.id != member.id:
				await self.bot.add_roles(member, matchingTag[0])
				addedusers += member.name + ' '
			
		
		await say('Added the following users to @'+matchingTag[0].name+':\n' + addedusers)
		return


	# ------------------------------------------------------------------------------
	# Function: Remove tag from a User
	# Description: Remove a tag from a user on the server
	# Usable by: Bot Commander
	# Scope: Server

	@commands.command(pass_context=True)
	async def untag(self, ctx, tag : str, *mentions: discord.Member):
		"""Untags a user
		
		Bot commanders may use this command to remove tags from other users
		"""
		the = MessageContext(ctx)
		
		# Check power
		if not is_BotCommander(ctx) and not is_Admin(ctx):
			await sayerror('Insufficient Permissions', 'You must be a `@Bot Commander` to use this command')
			print('tag: Not @Bot Commander')
			return
					
		matchingTag = get_tags(the.server, tag)
		if len(matchingTag) > 1:
			await sayerror('Duplicate tag @' + matchingTag[0].name + ' detected!','Please resolve the duplicate in server settings or use the `' + PREFIX + 'clean` command to resolve automatically')
			return
		elif len(matchingTag) == 0: 
			await sayerror('Tag does not exist')
			return
		
		removedusers = ''
		for member in mentions:
			if self.bot.user.id != member.id:
				await self.bot.remove_roles(member, matchingTag[0])
				removedusers += member.name + ' '
			
		
		await say('Removed the following users from @'+matchingTag[0].name+':\n' + removedusers)
		return


	# ------------------------------------------------------------------------------
	# Function: Clean Tags
	# Description: Scans server tags, removes tags which are named same as real roles, duplicates (merge tags), and empty tags
	# Usable by: Bot Commander
	# Scope: Server

	@commands.command(pass_context=True)
	async def clean(self, ctx):
		"""Cleans server tags
		
		Automatically removes duplicate, empty and invalid tags.
		"""
		the = MessageContext(ctx)

		# Check Permissions
		if not is_BotCommander(ctx) and not is_Admin(ctx):
			await sayerror('Insufficient Permissions', 'You must be a `@Bot Commander` to use this command')
			print('tag: Not @Bot Commander')
			return
		
		roleList = []
		roleNames = []
		cleaned = []
		
		for role in the.server.roles:
			if is_tag(role):
				if role.name not in roleNames:
					# Not a duplicate
					roleList.append(role)
					roleNames.append(role.name)
				else:
					# Duplicate found
					index = roleNames.index(role.name)
					for member in the.server.members:
						if role in member.roles:
							await self.bot.add_roles(member, roleList[index])
					cleaned.append(role.name)
					await self.bot.delete_role(the.server, role)
		if cleaned:
			list = ''
			for tag in cleaned:
				list += '@' + tag + '\t'
			
			await say('Cleaned: ' + list)
		else:
			await say('Nothing to clean!')
				
		

def setup(bot):
	bot.add_cog(Commanders(bot))