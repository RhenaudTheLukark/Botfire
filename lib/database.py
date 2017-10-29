import lib.globalvars

import discord
import asyncio
import sqlite3

class sql_commands:
	'''SQLite Database Commands'''
	print("Attempting connection to SQLite database...")
	try:
		conn = sqlite3.connect("data/botfire.sqlite")
		print("The connection to the database is successful!")
	except Exception as e:
		print(e)
	
	async def evalSqlOw(self, message, req):
		'''Evaluates any SQL command.
Requires Admin privileges.'''
		if not lib.globalvars.isAdmin(message.author):
			return
		result = ""
		for row in self.conn.cursor().execute(req):
			result += str(row) + str("\n")
		await lib.globalvars.client.send_message(message.channel, "Success!\n" + result)
	
	async def evalSql(self, message, req):
		'''Evaluates any SQL command beginning with "SELECT".
You need quotes around your full command.'''
		if req[0:7] != "SELECT ":
			await lib.globalvars.client.send_message(message.channel, "Only SELECT is permitted with this command!")
			return
		result = ""
		for row in self.conn.cursor().execute(req):
			result += str(row) + "\n"
		await lib.globalvars.client.send_message(message.channel, "Success!\n" + result)
	
	async def registerUsers(self, message):
		'''Adds all users in the server to the SQLite database.
Requires Admin privileges.'''
		if not lib.globalvars.isAdmin(message.author):
			return
		count = 0
		for user in lib.globalvars.client.get_all_members():
			try:
				self.conn.cursor().execute("INSERT INTO Users(ID) VALUES (" + user.id + ")")
				count += 1
			except:
				next
		self.conn.commit()
		await lib.globalvars.client.send_message(message.channel, "Success: " + str(count) + " users added!")
