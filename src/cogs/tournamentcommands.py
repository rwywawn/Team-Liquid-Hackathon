import asyncio
import boto3
import discord
from .tournyHelper import tournament
from discord.ext import commands


class Tournaments(commands.Cog, name="Tournament Interface Commands"):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.tournaments = {}

    @commands.command()
    async def tourny(self, ctx, *args):
        guild = ctx.message.guild
        author = ctx.message.author
        channel = ctx.message.channel

        # command list
        if args[0] == 'create':
            try:
                if len(args) < 4:
                    await channel.send("Please specify at least 2 teams!")
                else:
                    title = args[1]
                    teams = args[2:]
                    
                    tourny = tournament(teams, title)
                    self.tournaments[title] = tourny
                    await channel.send(f"Tournament {title} created")

            except Exception:
                await channel.send("Unknown error!")
        
        elif args[0] == 'matchwin':
            try:
                title = args[1]
                team = args[2]
                self.tournaments[title].update(team)
                await channel.send(f"{team} won the match!")

            except IndexError:  
                await channel.send("You are missing arguments! Check your command.")
            except Exception:
                await channel.send("Unknown error!")

        elif args[0] == 'status':
            try:
                title = args[1]
                matches = self.tournaments[title].getMatches()
                round_num = self.tournaments[title].getCurrentRound()
                #winner = self.tournaments[title].getWinner()
                #print(winner)
                #if winner:
                #    print("something won")
                #    print(winner)
                #    await channel.send(f"{winner} has won the tournament on round {round_num}!")
                #else:
                await channel.send(f"Presenting next match ups for round {round_num}...")
                for match in matches:
                    await channel.send(f"{match[0]} versus {match[1]}!")

            except IndexError:  
                await channel.send("You are missing arguments! Check your command.")
            except Exception:
                await channel.send("Unknown error!")


        else:
            await channel.send("Unrecognized command - Try running ~tourny help")