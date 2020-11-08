import asyncio
import boto3
from datetime import datetime, timedelta
from pytz import timezone

import discord
from discord.ext import commands

GUILD=774456734101012520

class Auth(commands.Cog, name='Authenticater'):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def verify(self, ctx):
        guild = ctx.message.guild
        author = ctx.message.author
        channel = ctx.message.channel

        
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('authentication')
        response = table.get_item(Key={'user_id':str(author.id)})
       
   
        if "Item" in response.keys():
            role = discord.utils.get(author.guild.roles, name="verified")
            await author.add_roles(role)

            await channel.send("You have been verified")
        else:
            await channel.send("Please verify through this link http://127.0.0.1:5000/")
