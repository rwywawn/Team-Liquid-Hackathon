import asyncio
import boto3
from datetime import datetime, timedelta
from pytz import timezone

import discord
from discord.ext import commands

GUILD=774456734101012520

class Auth(commands.Cog, name='Auth'):
    def __init__(self, bot):
        self.bot = bot
        self._last_member_ = None
    
    async def authenticate(self,ctx):
        guild = ctx.message.guild
        author = ctx.message.author
        channel = ctx.message.channel

        
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table
        )
        response = table.get_item(Key={'user_id':userId })
       
   
        if "Item" in response.keys():
            role=discord.utils.get(author.server.roles,name="verified")
            await ctx.message.client.add_roles(author,role)
            channel.message("You have been verified")
        channel.message("Please verify through this link http://127.0.0.1:5000/")

