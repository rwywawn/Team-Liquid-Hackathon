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
                category = discord.utils.get(guild.categories, name="Temporary-Rooms")
                if category == None:
                    category = await guild.create_category_channel("Temporary-Rooms")

                room_name = args[1]
                time = int(args[2])

                if time > 240:
                    await channel.send(f"Time set is too long! Set to 4 hours.")
                    time = 240

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
                        user_role: discord.PermissionOverwrite(view_channel=True),
                        admin_role: discord.PermissionOverwrite(view_channel=True,
                                                                ban_members=True,
                                                                kick_members=True),
                        else_role: discord.PermissionOverwrite(view_channel=False)
                }



                vc = await guild.create_voice_channel(room_name,
                                                        overwrites=vc_perms,
                                                        category=category)
                tc = await guild.create_text_channel(room_name,
                                                        overwrites=tc_perms,
                                                        category=category)

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
                    await channel.send("Room created!")
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
            except Exception:
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
                dbRoom = db.get_item(Key={'name': ctx.message.channel.name})
                if (ctx.message.author.id == dbRoom["Item"]["author"]):
                    try:
                        time = int(args[1])
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
                        await channel.send("Unknown error...")
                else:
                    await channel.send("You are not the room admin!")

            except:
                await channel.send("This is not a temporary room!")

        elif args[0] == 'invite':
            try:
                dbRoom = db.get_item(Key={'name': ctx.message.channel.name})

                if (ctx.message.author.id == dbRoom["Item"]["author"]):
                    try:
                        invited = ctx.message.mentions
                        assert len(invited) > 0

                        user_role = discord.utils.get(guild.roles, id=int(dbRoom["Item"]['user_id']))
                        new_users = dbRoom["Item"]['members']


                        for person in invited:
                            if person.id == dbRoom["Item"]['author']:
                                await channel.send("You can't invite yourself.")
                            elif person.id not in new_users:
                                await person.add_roles(user_role)
                                await channel.send(f"Added {person.display_name}.")

                                new_users.append(person.id)
                            else:
                                await channel.send(f"{person.display_name} is already here.")

                        db.update_item(
                            Key={'name': ctx.message.channel.name},
                            UpdateExpression="set members=:newMembers",
                            ExpressionAttributeValues = {
                                ":newMembers": new_users
                            }
                        )
                    except AssertionError: 
                        await channel.send("You didn't invite anyone else.")
                    except:
                        await channel.send("Unknown error...")
                else:
                    await channel.send("You aren't the room admin.")
            except:
                await channel.send("This is not a temporary room!")

        elif args[0] == 'kick':
            try: 
                dbRoom = db.get_item(Key={'name': ctx.message.channel.name})

                if (ctx.message.author.id == dbRoom["Item"]["author"]):
                    try:
                        kicked = ctx.message.mentions
                        assert len(kicked) > 0

                        user_role = discord.utils.get(guild.roles, id=int(dbRoom["Item"]['user_id']))
                        new_users = dbRoom["Item"]['members']

                        for person in kicked:
                            if person.id == dbRoom["Item"]['author']:
                                await channel.send("You can't kick yourself.")
                            elif person.id in new_users:
                                await person.remove_roles(user_role)
                                await channel.send(f"Kicked {person.display_name}.")
                                new_users.remove(person.id)
                            else:
                                await channel.send(f"{person.display_name} isn't in the room!")

                        db.update_item(
                            Key={'name': ctx.message.channel.name},
                            UpdateExpression="set members=:newMembers",
                            ExpressionAttributeValues = {
                                ":newMembers": new_users
                            }
                        )
                    except AssertionError:
                        await channel.send("You didn't kick anyone.")
                    except:
                        await channel.send("Unknown error...")
                else:
                    await channel.send("You aren't the room admin.")
            except:
                await channel.send("This is not a temporary room!")

        elif args[0] == 'help':
            response = "The available commands for the room are create, time, extend, add, remove, status, and help. To destroy a room, run ~destroy."
            await channel.send(response)

        elif args[0] == 'destroy':

            toDestroy = db.get_item(Key={'name': ctx.message.channel.name})

            if (ctx.message.author.id == toDestroy["Item"]["author"]):

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

        else:
            await channel.send("Unrecognized command - Try running ~room help.")
