import os
import random

import asyncio
import boto3
from datetime import datetime, timedelta
from pytz import timezone

import discord
from discord.ext import commands

global daemonRunning
daemonRunning = False
ROOM_SLEEPER = 2
GUILD = 774456734101012520

dynamo = boto3.resource('dynamodb')
db = dynamo.Table('rooms')

async def RoomThread(bot):

    while True:
        response = db.scan()
        items = response["Items"]
        for room in items:
            expiry_time = datetime.strptime(room['expires'], "%Y-%m-%dT%H:%M:%S.%fZ")
            time_diff = expiry_time - datetime.now()

            if time_diff < timedelta():
                tc = discord.utils.get(bot.get_guild(GUILD).text_channels, id=int(room['tc_id']))
                vc = discord.utils.get(bot.get_guild(GUILD).voice_channels, id=int(room['vc_id']))

                member_role = discord.utils.get(bot.get_guild(GUILD).roles, id=int(room['admin_id']))
                admin_role = discord.utils.get(bot.get_guild(GUILD).roles, id=int(room['user_id']))

                await tc.delete()
                await vc.delete()
                await member_role.delete()
                await admin_role.delete()

                db.delete_item(Key={'name': room['name']})

        await asyncio.sleep(ROOM_SLEEPER)


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
            asyncio.get_event_loop().create_task(RoomThread(self.bot))
            print('Room thread started.')