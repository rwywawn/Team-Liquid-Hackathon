import discord
import os
from discord.ext import commands
from config import Config
import time
client = discord.Client()

client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#will load all cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}') #take off last 3 characters since the .py part isn't needed

#for our bot authentication
client.run(Config['token'])