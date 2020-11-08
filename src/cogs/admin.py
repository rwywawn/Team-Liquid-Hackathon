import os
import json
import asyncio
import boto3
from datetime import datetime, timedelta

import discord
from threading import Timer
from discord.ext import commands

bot = discord.Client()

global daemonRunning
daemonRunning = False
EVENT_SLEEPER = 2

dynamo = boto3.resource('dynamodb')
events = dynamo.Table('events')
sub = dynamo.Table('sub')


async def EventThread():
    channel = bot.get_channel(774945538977431552)
    while True:
        print('Event Threading...')

        response_event = events.scan()
        items_event = response_event["Items"]

        response_sub = sub.scan()
        items_sub = response_sub["Items"]

        for i in items_event:
            now = datetime.now()
            date_total = i['date']
            future_date = datetime.strptime(date_total, '%Y-%m-%d %H:%M')
            difference = (future_date - now).total_seconds()

        await asyncio.sleep(EVENT_SLEEPER)


class Admin(commands.Cog, name='Admin'):
    def init(self, bot):
        self.bot = bot
        self._lastmember = None

    @commands.Cog.listener()
    async def on_ready(self):
        print("Connected to Discord.")
        global daemonRunning
        if not daemonRunning:
            daemonRunning = True
            asyncio.get_event_loop().create_task(EventThread())
            print('Event thread started.')