import discord 
from discord.ext import commands

import asyncio
import json
import boto3

from datetime import datetime
from threading import Timer
import argparse
now = datetime.now()

dynamo = boto3.resource('dynamodb')
events = dynamo.Table('events')

def hello():
    print("HIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")

class Events(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot 

    @commands.command()
    async def event(self, ctx, *args):
        channel = ctx.message.channel
        messageAuthor = ctx.author
        guild = messageAuthor.guild

        #commands list
        if args[0] == 'plan':
            try:
                event_name = args[1]
                event_date = args[2]
                event_time = args[3]
                event_link = args[4]

                print(event_name, event_date, event_time, event_link)

                date_total = event_date + ' ' + event_time
                now = datetime.now()
                future_date = datetime.strptime(date_total, '%Y-%m-%d %H:%M')
                difference = (future_date - now).total_seconds()
                
                event_info = {
                    "event_name": event_name,
                    "date": date_total,
                    "link": event_link
                }

                events.put_item(Item=event_info)
                await channel.send("Event info added to database")

                response = f'{event_name} happening on {event_date} at {event_time}, at: {event_link}'
                await channel.send(response)
                t = Timer(difference, hello)
                t.start()

            except IndexError:
                response = "Please check your agruments!"
                await channel.send(response)
        
        elif args[0] == 'upcoming':

            response = events.scan()
            items = response['Items']
            for i in (items):
                await channel.send(f"**EVENT**: {i['event_name']} **ON**: {i['date']} **AT** :{i['link']}")
        
        elif args[0] == 'delete':
            try:
                event_name = args[1]
                events.delete_item(Key={'event_name': event_name})
                await channel.send('Event cancelled')
            except IndexError:
                await channel.send('Invalid Event Name')


        else:
            await channel.send("This was not an available command please use help to see available commands")




def setup(bot):
    bot.add_cog(Events(bot)) 