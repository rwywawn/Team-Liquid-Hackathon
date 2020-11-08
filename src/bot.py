import os
import sys

from config import Config

import discord
from discord.ext import commands

from cogs.roomcommands import Rooms
from cogs.admin import Admin
from cogs.events import Events

bot = discord.Client()

def main():
    bot = commands.Bot(command_prefix=Config['prefix'])
    bot.add_cog(Rooms(bot))
    bot.add_cog(Admin(bot))
    bot.add_cog(Events(bot))
    bot.run(Config['token'])


if __name__ == "__main__":
    main()
