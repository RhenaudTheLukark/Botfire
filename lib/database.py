import lib.globalvars

import discord
import asyncio
import sqlite3

class sql_commands:
	'''Campfire Quest Commands'''
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
		self.conn.commit()
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
		self.conn.commit()
		await lib.globalvars.client.send_message(message.channel, "Success!\n" + result)
	
	async def registerUsers(self, message):
		'''A test function (?).
Adds all users in the server to the SQLite database.
Requires Admin privileges.'''
		if not lib.globalvars.isAdmin(message.author):
			return
		count = 0
		for user in lib.globalvars.client.get_all_members():
			try:
				self.conn.cursor().execute("INSERT INTO Users(ID, playing) VALUES (" + user.id + ", 0)")
				count += 1
			except:
				next
		self.conn.commit()
		await lib.globalvars.client.send_message(message.channel, "Success: " + str(count) + " users added!")
	
	async def removeMe(self, message, mode="deactivate"):
		'''Attempts to remove you from the SQLite table.
Type 'full' for the second argument to completely remove yourself from the table (no quotes).
WARNING! If you delete your data, it can not be recovered!'''
		if len([row for row in self.conn.cursor().execute("SELECT * FROM Users WHERE ID='" + message.author.id + "'")]) == 0:
			await lib.globalvars.client.send_message(message.channel, "You are not an active player!")
			return
		if mode.lower() == "full":
			self.conn.cursor().execute("DELETE FROM Users WHERE ID='" + message.author.id + "'")
			self.conn.commit()
			await lib.globalvars.client.send_message(message.channel, "You have been removed from the table.")
		else:
			self.conn.cursor().execute("UPDATE Users SET playing=0 WHERE ID='" + message.author.id + "'")
			self.conn.commit()
			await lib.globalvars.client.send_message(message.channel, "You are no longer an active player.")
	
	async def addMe(self, message):
		'''If you are already in the table, sets "playing" to 1 for you.
If you are not in the table, you will be added.'''
		test = len([row for row in self.conn.cursor().execute("SELECT * FROM Users WHERE ID='" + message.author.id + "'")])
		if test > 1:
			self.conn.cursor.execute("DELETE FROM Users WHERE ID='" + message.author.id + "'")
			self.conn.commit()
			test = 0
		if test == 0:
			self.conn.cursor().execute("INSERT INTO Users(ID, playing) VALUES (" + message.author.id + ", 1)")
		elif test == 1:
			if len([row for row in self.conn.cursor().execute("SELECT * FROM Users WHERE ID='" + message.author.id + "' AND playing=1")]) == 0:
				self.conn.cursor().execute("UPDATE Users SET playing=1 WHERE ID='" + message.author.id + "'")
			else:
				await lib.globalvars.client.send_message(message.channel, "You are already registered!")
				return
		self.conn.commit()
		await lib.globalvars.client.send_message(message.channel, "You are now an active player!\n\nUse `" + lib.globalvars.prefix + "removeMe` to quit.")
