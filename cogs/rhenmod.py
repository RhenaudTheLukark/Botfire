import discord
from discord.ext import commands
from .utils.chat_formatting import escape_mass_mentions, italics, pagify
from random import randint
from random import choice
from enum import Enum
from urllib.parse import quote_plus
import datetime
import time
import aiohttp
import asyncio

class RhenMod:
    """General commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sayHi(self):
        """Lea! ...why?"""
        await self.bot.say('Hi! Lea!')


    @commands.command()
    async def say(self, str):
        """Repeats a text, that's about it, really"""
        await self.bot.say(str)

def setup(bot):
    bot.add_cog(RhenMod(bot))