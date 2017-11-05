import lib.globalvars

import os
import discord
import asyncio
import sys
import inspect
import datetime

class general_commands:
	'''General Commands'''
	
	start_time = datetime.datetime.now()
	
	async def shutdown(self, message):
		'''Shuts down the bot.
Requires Admin privileges.'''
		if lib.globalvars.isAdmin(message.author):
			await lib.globalvars.client.send_message(message.channel, "Shutting down, byebye! \N{WAVING HAND SIGN}\N{EMOJI MODIFIER FITZPATRICK TYPE-3}")
			await lib.globalvars.client.close()
	
	async def commands(self, message, command=""):
		'''Shows a list of all commands.'''
		classlist = [item.__class__ for item in lib.globalvars.class_list]
		result = "```"
		def getformat(method):
			if len(inspect.signature(method).parameters) > 2:
				return lib.globalvars.prefix + method.__name__ + " " + str(inspect.signature(method)).replace("self, message, ", "").replace("self, message)", ")")#[1:-1]
			else:
				return lib.globalvars.prefix + method.__name__
		if command == "":
			foundadmincommand = False
			for clas in classlist:
				methods = [func for func in dir(clas) if inspect.iscoroutinefunction(getattr(clas, func)) and not func.startswith("__")]
				if len(methods) > 0:
					if clas.__doc__ != None:
						result += "\n%s" % clas.__doc__
					else:
						result += "\n%s" % clas.__name__
					result += ":"
					for method in methods:
						if getattr(clas, method).__doc__ != None and getattr(clas, method).__doc__.lower().endswith("requires admin privileges."):
							result += "\n *  "
							foundadmincommand = True
						else:
							result += "\n    "
						result += getformat(getattr(clas, method))
			if foundadmincommand:
				result += "\n\n(* = Admin privileges required)"
			result += "```\nType `" + lib.globalvars.prefix + "commands <command>` for specific information on a command."
			if lib.globalvars.send_command_list_to_dm:
				try:
					await lib.globalvars.client.send_message(message.author, result)
				except discord.Forbidden:
					await lib.globalvars.client.send_message(message.channel, "I was unable to send you the list of commands.\nEither you have your privacy settings set to disallow direct messages from other server members,\nor you have this bot blocked.")
			else:
				await lib.globalvars.client.send_message(message.channel, result)
		else:
			if command.startswith(lib.globalvars.prefix):
				command = command.split(lib.globalvars.prefix)[1]
			for clas in classlist:
				methods = [func for func in dir(clas) if inspect.iscoroutinefunction(getattr(clas, func)) and not func.startswith("__")]
				if command in methods:
					result += "\n" + getformat(getattr(clas, command)) + "\n\n"
					if getattr(clas, command).__doc__ != None:
						result += getattr(clas, command).__doc__
					else:
						result += "No description available."
					result += "\n```"
					await lib.globalvars.client.send_message(message.channel, result)
					return
			result = "Command '%s' not found.\nUse `" + lib.globalvars.prefix + "commands` for a list of all usable commands." % command
			await lib.globalvars.client.send_message(message.channel, result)
	
	async def uptime(self, message):
		'''Returns the amount of time the bot client has been running.'''
		difference = datetime.datetime.now() - self.start_time
		days = difference.days
		hours = difference.seconds//3600
		minutes = (difference.seconds//60)%60
		seconds = difference.seconds%60
		await lib.globalvars.client.send_message(message.channel, "**%s** has been up for:\n%s days, %s hours, %s minutes, %s seconds" % (lib.globalvars.client.user.name, days, hours, minutes, seconds))
