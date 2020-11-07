import os
import sys
from config import Config
from dotenv import load_dotenv
load_dotenv()

import discord
from discord.ext import commands

from commands.roomcommands import roomcommands

def main():
	bot = commands.Bot(command_prefix="~")
	bot.remove_command('help')
	bot.add_cog(roomcommands(bot))
	bot.run(Config.token)


if __name__ == "__main__":
	main()
