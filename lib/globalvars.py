from data.config import *
import discord
import asyncio
client = discord.Client()

async def checkAdmin(message):
	if perm_role in [role.name for role in message.author.roles]:
		return true
	else:
		if error_handling_mode == 0:
			await client.add_reaction(message, "\U0001F6AB")
		elif error_handling_mode == 1:
			await client.send_message(message.channel, "You do not have the permissions required to use this command.")
		print("%s lacks privileges!" % message.author.name)
		return False
