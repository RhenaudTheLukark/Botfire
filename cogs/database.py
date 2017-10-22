import discord
from discord.ext import commands
from cogs.utils import checks
from .utils.chat_formatting import escape_mass_mentions, italics, pagify
from random import randint
from random import choice
from enum import Enum
from urllib.parse import quote_plus
import datetime
import time
import aiohttp
import asyncio
import sqlite3

class Database:
    """General commands."""

    conn = None

    def __init__(self, bot):
        self.bot = bot
        print("Trying to open SQLite database...")
        self.conn = sqlite3.connect('data/botfire.sqlite')
        print("The connection to the database is successful!")

    @commands.command()
    async def evalSql(self, req):
        """Permits to do some SQL shenans (SELECT only)."""
        if req[:7] != 'SELECT ':
        	await self.bot.say('Your SQL command has to be a SELECT and nothing else!')
        	return

        result = ""
        c = self.conn.cursor()
        for row in c.execute(req):
            result += str(row) + "\n"

        await self.bot.say(result + "Success!")

    @commands.command()
    @checks.mod_or_permissions(administrator=True)
    async def evalSqlOw(self, req):
        result = ""
        c = self.conn.cursor()
        for row in c.execute(req):
            result = str(result) + str(row) + str('\n')

        await self.bot.say(result + "Success!")

    @commands.command()
    @checks.mod_or_permissions(administrator=True)
    async def registerUsers(self):
        c = self.conn.cursor()
        self.count = 0
        for user in self.bot.get_all_members():
            try:
            	c.execute('INSERT INTO Users(ID) VALUES (' + user.id + ')')
            	self.count = self.count + 1
            except:
            	next
        self.conn.commit()
        await self.bot.say("Success: " + str(self.count) + " users added!")

def setup(bot):
    bot.add_cog(Database(bot))
