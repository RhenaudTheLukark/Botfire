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

    @commands.command(pass_context=True)
    async def sayHi(self, ctx):
        """Lea! ...why?"""
        try:
            await self.bot.delete_message(ctx.message)
        except:
            print("Shit can't deleet!")
        try:
            await self.bot.say('Hi! Lea!')
        except:
            print("Ah fuck can't talk dammit")


    @commands.command(pass_context=True)
    async def say(self, ctx, str):
        """Repeats a text, that's about it, really"""
        try:
            await self.bot.delete_message(ctx.message)
        except:
            print("Shit can't deleet!")
        try:
            await self.bot.say(str)
        except:
            print("Ah fuck can't talk dammit")

def setup(bot):
    bot.add_cog(RhenMod(bot))