<<<<<<< HEAD
import os
import sys

from config import Config

import discord
from discord.ext import commands

from cogs.roomcommands import Rooms
from cogs.admin import Admin

bot = discord.Client()

def main():
    bot = commands.Bot(command_prefix=Config['prefix'])
    bot.add_cog(Rooms(bot))
    bot.add_cog(Admin(bot))
    bot.run(Config['token'])


if __name__ == "__main__":
    main()
=======
import discord
from config import Config
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print('https://discord.com/api/oauth2/authorize?client_id=774513868365234226&redirect_uri=http%3A%2F%2Flocalhost%2F&response_type=code&scope=connectionsD')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(Config['token'])
>>>>>>> main
