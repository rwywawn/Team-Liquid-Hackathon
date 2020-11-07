import os
import sys
from dotenv import load_dotenv
load_dotenv()

import discord
from discord.ext import commands

from commands.roomcommands import roomcommands

def main():
	bot = commands.Bot(command_prefix="~")
	bot.remove_command('help')
	bot.add_cog(roomcommands(bot))
	bot.run("Nzc0NTEwNjk0MjY3NjE3MzMw.X6Y1Sw.QqwJ4xsw7mYGAFAtKcwaCW8zZmU")


if __name__ == "__main__":
	main()
