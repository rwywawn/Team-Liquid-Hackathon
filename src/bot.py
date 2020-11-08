import discord
import os
import sys
from discord.ext import commands
from config import Config
import time
from cogs.events import Events
from cogs.admin import Admin

bot = discord.Client()

bot = commands.Bot(command_prefix = '!')

def main():
    bot.add_cog(Events(bot))
    bot.add_cog(Admin(bot))
    bot.run(Config['token'])


if __name__ == "__main__":
    main()
