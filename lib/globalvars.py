from data.config import prefix
from data.config import perm_role
from data.config import send_command_list_to_dm
import discord
client = discord.Client()

def isAdmin(member):
	return perm_role in [role.name for role in member.roles]