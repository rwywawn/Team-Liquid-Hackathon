import asyncio
import json
import redis

from datetime import datetime
from datetime import timedelta

import discord
from discord.ext import commands

class Rooms(commands.Cog, name='Room Creation Commands'):
        def __init__(self, bot):
                self.bot = bot
                self._last_member = None

        @commands.command()
        async def create_room(self, ctx, *args):
                guild = ctx.message.guild
                author = ctx.message.guild

                room_name = f"{author.display_name.replace(' ', '-').lower()}-game-room"

                # command list
                if args[0] == 'create':
                        try:
                                room = ""
                        except:
                                response = "error"
                                await channel.send(response)

                elif args[0] == 'time':
                        try:
                                room = ""
                        except:
                                response = "error"
                                await channel.send(response)

                elif args[0] == 'extend':
                        try:
                                room =
                        except:
                                response = "error"
                                await channel.send(response)

                elif args[0] == 'invite':
                        try:
                                room = ""
                        except:
                                response = "error"
                                await channel.send(response)

                elif args[0] == 'kick':
                        try:
                                room = ""
                        except:
                                response = "error"
                                await channel.send(response)

                elif args[0] == 'status':
                        try:
                                room = ""
                        except:
                                response = "error"
                                await channel.send(response)

                elif args[0] = 'help':
                        response = "The available commands are create, time, extend, add, remove, status, and help."
                        await channel.send(response)


        @commands.command()
        async def destroy_room(self, ctx):
                guild = ctx.message.guild
                author = ctx.message.author
                
                room_name = "something"
                
                # clearing channels and roles created
                text_channel = discord.utils.get(guild.text_channels, channel_name)
                voice_channel = discord.utils.get(guild.voice_channels, channel_name)
                admin_role = discord.utils.get(guild.roles, admin)
                member_role = discord.utils.get(guild.roles, member)

                await text_channel.delete()
                await voice_channel.delete()
                await member_role.delete()
                await admin_role.delete()
                

                