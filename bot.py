from __all_imports import *

class_list = [lib.general.general_commands(), lib.database.sql_commands()]
lib.globalvars.class_list = class_list

@lib.globalvars.client.event
async def on_ready():
	print("------\nBot ready!\n%s\n%s\n------" % (lib.globalvars.client.user.name, lib.globalvars.client.user.id))
	# await console_input()

async def console_input():
	while True:
		if input("").lower() in ["shutdown", "quit", "exit", "leave", "turn off", "shut down", "close"]:
			await lib.globalvars.client.close()
			break

@lib.globalvars.client.event
async def on_message(message):
	await lib.globalvars.client.wait_until_ready()
	if message.content.startswith(lib.globalvars.prefix) and message.author is not lib.globalvars.client:
		try:
			for clas in class_list:
				method_list = [func for func in dir(clas) if callable(getattr(clas, func)) and not func.startswith("__")]
				parsed = parse(message.content)
				for func in method_list:
					if parsed[0] == lib.globalvars.prefix + func:
						arggs = [message] + parse(message.content)[1:]
						params = signature(getattr(clas, func)).parameters
						#if len(arggs) > len(params) and len(arggs) > 0:
							#arggs[len(params)-1:len(arggs)] = [" ".join(arggs[len(params)-1:len(arggs)])]
						await getattr(clas, func)(*arggs)
						# bonus feature: "good bot"
						def check(msg):
							return msg.author != lib.globalvars.client.user and not msg.author.bot
						msg = await lib.globalvars.client.wait_for_message(check=check, channel=message.channel)
						if msg.content.lower().startswith("good bot"):
							await lib.globalvars.client.send_message(message.channel, "Good human")
						return
		except Exception as e:
			# if a command would cause an error (or the command is not found), react with "?" and wait up to 20 seconds
			if lib.globalvars.error_handling_mode == 1:
				await lib.globalvars.client.send_message(message.channel, "```\n%s:\n%s\n```" % (str(e.__name__), str(e)))
				return
			print(e)
			if lib.globalvars.error_handling_mode == 2:
				return
			try:
				if not "\U00002753" in [reaction.emoji for reaction in message.reactions]:
					await lib.globalvars.client.add_reaction(message, "\U00002753")
					for i in range(20):
						if message.edited_timestamp != None:
							break
						await asyncio.sleep(1)
					if "\U00002753" in [reaction.emoji for reaction in message.reactions if reaction.me]:
						await lib.globalvars.client.add_reaction(message, "\U00002753")
					await on_message(message)
				else:
					await lib.globalvars.client.remove_reaction(message=message, emoji="\U00002753", member=lib.globalvars.client.user)
			except:
				return

def parse(input):
	output = []
	if len(input.split(" ")) > 1:
		output = [input[0:input.find(" ")]]
		findall = re.findall('"([^"]+)"|\'([^\']+)\'|([^\s]+)', input.split(input.split(" ")[0])[1])
		for item in findall:
			output.append("".join(item))
	elif len(input.split(" ")) == 1:
		output = [input]
	return output

lib.globalvars.client.run(open("data/token.txt", "r").read(), bot=True)
