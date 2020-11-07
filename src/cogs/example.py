import discord 
from discord.ext import commands

class Example(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot #access client within cog

    #events
    @commands.Cog.listener()
    async def on_ready(self):
        print('IM HERE')

    #commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('POG')
    
#connect cog with bot
def setup(bot):
    bot.add_cog(Example(bot)) 