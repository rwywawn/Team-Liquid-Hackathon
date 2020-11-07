import discord

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run('Nzc0NDc1MDI0MDU5OTkwMDU3.X6YUEg.7JV-sEMopCk72r-1jflxgScY78g')