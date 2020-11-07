import asyncio
import json
import boto3

from datetime import datetime
from datetime import timedelta

import discord
from discord.ext import commands

dynamo = boto3.resource('dynamodb')
db = dynamo.Table('rooms')

class Rooms(commands.Cog, name='Room Creation Commands'):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def room(self, ctx, *args):
        guild = ctx.message.guild
        author = ctx.message.author
        channel = ctx.message.channel

        # command list
        if args[0] == 'create':
            try:
                room_name = args[1]
                time = int(args[2])

                if time > 240:
                    await channel.send(f"Time set is too long! Set to 4 hours.")
                    time = 240

                await channel.send(f"room to be created with name: {room_name} and time: {time}")

                admin_role = await guild.create_role(name=f"{room_name}-admin")
                user_role = await guild.create_role(name=f"{room_name}-user")
                else_role = discord.utils.get(guild.roles, name='@everyone')

                await author.add_roles(admin_role)

                vc_perms = {
                        user_role: discord.PermissionOverwrite(view_channel=True),

                        admin_role: discord.PermissionOverwrite(view_channel=True,
                                                                mute_members=True,
                                                                deafen_members=True,
                                                                ban_members=True,
                                                                kick_members=True,
                                                                priority_speaker=True),

                        else_role: discord.PermissionOverwrite(view_channel=False)
                }

                tc_perms = {
                        user_role: discord.PermissionOverwrite(view_channel=False),
                        admin_role: discord.PermissionOverwrite(view_channel=True),
                        else_role: discord.PermissionOverwrite(view_channel=True,
                                                                ban_members=True,
                                                                kick_members=True)
                }



                vc = await guild.create_voice_channel(room_name,
                                                        overwrites=vc_perms)
                tc = await guild.create_text_channel(room_name,
                                                        overwrites=tc_perms)

                room_info = {
                    "name": room_name,
                    "vc_id": vc.id,
                    "tc_id": tc.id,
                    "created": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    "expires": (datetime.now() + timedelta(minutes=time)).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    "author": author.id,
                    "members": [],
                    "admin_id": admin_role.id,
                    "user_id": user_role.id
                }

                try:
                    db.put_item(Item=room_info)
                    await channel.send("Room info added to database.")
                except:
                    await tc.delete()
                    await vc.delete()
                    await user_role.delete()
                    await admin_role.delete()
                    await channel.send("Database error!") 
                    
            except IndexError:
                await channel.send("You are missing arguments! Check your command.")
            except ValueError:
                await channel.send("You have to pass in a number for time! Check your command.")
            except:
                await channel.send("Unknown error the fuck did you do")

        elif args[0] == 'time':
            try:
                dbRoom = db.get_item(Key={'name': ctx.message.channel.name})
                room = dbRoom["Item"]["name"]
                expiry = datetime.strptime(dbRoom["Item"]["expires"], "%Y-%m-%dT%H:%M:%S.%fZ")
                remaining = expiry - datetime.now()

                await channel.send(f"{room} will expire after {remaining.seconds // 60} minutes.")
            except:
                await channel.send("Room is not a temporary room!")

        elif args[0] == 'extend':
            try:
                time = int(args[1])
                dbRoom = db.get_item(Key={'name': ctx.message.channel.name})
                expiry = datetime.strptime(dbRoom["Item"]["expires"], "%Y-%m-%dT%H:%M:%S.%fZ")

                expiry = expiry + timedelta(minutes=time)
                
                db.update_item(
                    Key={'name': ctx.message.channel.name},
                    UpdateExpression="set expires=:newExpires",
                    ExpressionAttributeValues = {
                        ":newExpires": expiry.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                    }
                )
                await channel.send(f"{time} minutes added.")

            except IndexError:
                await channel.send("You did not set a time to add!")
            except ValueError:
                await channel.send("You must input a number!")
            except:
                await channel.send("This is not a temporary room!")

        elif args[0] == 'invite':
            # try:
            invited = ctx.message.mentions
            dbRoom = db.get_item(Key={'name': ctx.message.channel.name})
            user_role = discord.utils.get(guild.roles, id=int(dbRoom["Item"]['user_id']))
            new_members = dbRoom["Item"]['members']

            # for person in invited:
            #     await member.add_roles(user_role)
            #     await channel.send(f"Added {member.display_name}.")

            await channel.send(new_members)
            # except: 
                # await channel.send("cum")

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

        elif args[0] == 'help':
            response = "The available commands are create, time, extend, add, remove, status, and help."
            await channel.send(response)


    @commands.command()
    async def destroy(self, ctx):
        guild = ctx.message.guild
        author = ctx.message.author
        channel = ctx.message.channel

        toDestroy = db.get_item(Key={'name': ctx.message.channel.name})

        if (ctx.message.author.id == toDestroy["Item"]["author"]):
            # clearing channels and roles created
            tc = discord.utils.get(guild.text_channels, id=int(toDestroy["Item"]['tc_id']))
            vc = discord.utils.get(guild.voice_channels, id=int(toDestroy["Item"]['vc_id']))

            admin_role = discord.utils.get(guild.roles, id=int(toDestroy["Item"]['admin_id']))
            user_role = discord.utils.get(guild.roles, id=int(toDestroy["Item"]['user_id']))

            await tc.delete()
            await vc.delete()
            await user_role.delete()
            await admin_role.delete()

            db.delete_item(Key={'name': ctx.message.channel.name})
        else:
            await channel.send("You are not the rooms owner!")
