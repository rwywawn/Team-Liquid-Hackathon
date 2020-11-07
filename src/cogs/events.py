import discord 
from discord.ext import commands

import datetime
import argparse

class Events(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot 

    #events
    @commands.Cog.listener()
    async def on_ready(self):
        print('events here')

    @commands.command()
    async def event(self, ctx, *args):
        channel = ctx.message.channel
        #commands list
        if args[0] == 'plan':
            try:
                event_name = args[1]
                event_date = args[2]
                event_time = agrs[3]

                list_date = event_date.split("/")
                list_time = event_time.split(":")


                response = f'{event_name} happening on {event_date} at {event_time}'
                await channel.send(response)

            except IndexError:
                response = "NIGGER WHERE ARE YOUR AGRUMENTS"
                await channel.send(response)
            except ValueError:
                response = "NIGGER THESE AREN'T REAL VALUES"
                await channel.send(response)
        else:
            await channel.send("This was not an available command please use plan help to see available commands")
        





def setup(bot):
    bot.add_cog(Events(bot)) 