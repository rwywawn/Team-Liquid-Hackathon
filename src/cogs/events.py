import discord 
from discord.ext import commands
import time

import asyncio
import json
import boto3

from datetime import datetime
from threading import Timer
import argparse
now = datetime.now()

dynamo = boto3.resource('dynamodb')
events = dynamo.Table('events')
sub = dynamo.Table('sub')

class Events(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot 

    @commands.command()
    async def event(self, ctx, *args):
        channel = ctx.message.channel

        #commands list
        if args[0] == 'plan':
            try:
                event_name = args[1]
                event_date = args[2]
                event_time = args[3]
                event_link = args[4]

                print(event_name, event_date, event_time, event_link)

                date_total = event_date + ' ' + event_time
                future_date = datetime.strptime(date_total, '%Y-%m-%d %H:%M')
                difference = (future_date - datetime.now()).total_seconds()
                event_info = {
                    "event_name": event_name,
                    "date": date_total,
                    "link": event_link
                }
                events.put_item(Item=event_info)
                await channel.send("Event info added to database, event created")

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

        elif args[0] == 'subscribe':
            user_id = ctx.message.author.id
            in_sub = False
            response = sub.scan()
            items = response['Items']
            for i in (items):
                if user_id == {i['sub_user']}:
                    in_sub = True

            if in_sub == False:
                user_info = {
                    "sub_user": user_id
                }
                sub.put_item(Item=user_info)
                await channel.send("Subscribed! You will receive notifications from us!")
            else:
                await channel.send("You are already subscribed!")
            
        elif args[0] == 'mention':
            response_user = sub.scan()
            items_user = response_user['Items']
            response_event = events.scan()
            items_event = response_event['Items']
            for i in items_event:
                now = datetime.now()
                date_total = i['date']
                future_date = datetime.strptime(date_total, '%Y-%m-%d %H:%M')
                difference = (future_date - now).total_seconds()

                if difference < 60:
                    for users in items_user:
                        await channel.send(f"**REMINDER**: <@{users['sub_user']}> EVENT STARTING NOW {i['event_name']} AT {i['link']}")

        else:
            await channel.send("This was not an available command please use help to see available commands")
