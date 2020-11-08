import os
import random
# import requests
import asyncio
import boto3
from datetime import datetime, timedelta
from pytz import timezone

import discord
from discord.ext import commands

global daemonRunning
daemonRunning = False
THREAD_SLEEPER = 5

dynamo = boto3.resource('dynamodb')
db = dynamo.Table('rooms')

async def RoomThread():
    while True:
        est = timezone('US/Eastern')
        currentTime = datetime.now().astimezone(est)

        roomsDB = db.scan()
        rooms_info = roomsDB['Items']
        for room in rooms_info:
            print(room)


class Admin(commands.Cog, name='Admin'):
    def __init__(self, bot):
        self.bot = bot
        self._last_member_ = None
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Connected to Discord.")
        global daemonRunning
        if not daemonRunning:
            daemonRunning = True
            asyncio.get_event_loop().create_task(RoomThread())
            print('Room thread started.')