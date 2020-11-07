import discord 
from discord.ext import commands

client = commands.Bot(command_prefix = '!')

@client.command()
async def load(ctx, extension):
    