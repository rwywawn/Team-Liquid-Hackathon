import os
import sys
import boto3

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
